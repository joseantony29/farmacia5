import json
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.db import transaction
from django.contrib import messages
from django.db.models import Q
from datetime import date, datetime
from django.views.generic import (
	TemplateView,
	ListView,
	DetailView,
	View
)
from apps.entidades.mixins import ValidarUsuario, RedirectIfExistsContabilidadMixin

from ...forms import EgresoForm

from ...models import Egreso, DetalleEgreso, TipoMov, Historial
from apps.inventario.models import Inventario, Producto
from apps.entidades.models import Perfil

class RegistrarEgreso(ValidarUsuario, RedirectIfExistsContabilidadMixin ,TemplateView):
	permission_required = 'movimientos.add_egreso'
	template_name = 'pages/movimientos/egreso/registrar_egreso.html'
	# permission_required = 'anuncios.requiere_secretria'
	object = None

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			with transaction.atomic():
				vents = json.loads(request.POST['vents'])

				tipo_egreso = TipoMov.objects.filter(pk=vents['tipo_egreso']).first()
				egreso = Egreso()
				egreso.fecha = vents['fecha']
				egreso.descripcion = vents['descripcion']
				egreso.tipo_egreso = tipo_egreso
				egreso.save()

				for det in vents['det']:
					producto = Producto.objects.filter(pk=det['id']).first()
					inventario = Inventario.objects.filter(pk=det['id_lote']).first()
					inventario.stock -= det['cantidad'] 
					inventario.save()

					detalle = DetalleEgreso()
					detalle.egreso = egreso
					detalle.inventario = inventario
					detalle.cantidad = det['cantidad']
					detalle.save()

					perfil = Perfil.objects.filter(usuario=request.user).first()
					movimiento = {
						'tipo_mov': tipo_egreso,
						'perfil': perfil,
						'producto': inventario,
						'cantidad': det['cantidad']
					}
					Historial().crear_movimiento(movimiento)
					producto.contar_productos()

				messages.success(request,'Egreso registrado correctamente')
				data['response'] = {'title': 'Exito!', 'data':'Egreso registrado correctamente', 'type_response': 'success'}
		except Exception as e:
			data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Registrar egreso"
		context["form"] = EgresoForm()
		return context

class BuscarProductosEgresoView(ValidarUsuario, View):
	permission_required = 'entidades.ver_inicio'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		# try:
		action = request.POST.get('action')
		ids_exclude = json.loads(request.POST.get('ids'))
		ids_exclude = [elemento for elemento in ids_exclude if elemento != '']
		if action == 'search_productos':
			data = []
			productos = Producto.objects.filter(nombre__icontains=request.POST.get('term'))
			for i in productos[0:10]:
				item = i.toJSON()
				item['text'] = '{}'.format(i.nombre)
				item['inv'] = {}
				item['inv']['datos'] = {}
				item['inv']['lotes'] = []
				item['id'] = i.pk
				for inv in Inventario.objects.filter(Q(comprometido__gt=0) | Q(stock__gt=0), producto_id=i.pk).exclude(pk__in=ids_exclude):
					item['inv']['datos'][f'{inv.pk}'] = inv.toJSON()
					item['inv']['lotes'].append({'id':inv.pk, 'text':f'{inv.lote} : {inv.stock}'})
				data.append(item)

		elif action == 'search_productos_table':
			data = []
			productos = Producto.objects.all()
			for i in productos:
				item = i.toJSON()
				item['text'] = '{}'.format(i.nombre)
				item['inv'] = {}
				item['inv']['datos'] = {}
				item['inv']['lotes'] = []
				item['id'] = i.pk
				for inv in Inventario.objects.filter(Q(comprometido__gt=0) | Q(stock__gt=0), producto_id=i.pk).exclude(pk__in=ids_exclude):
					item['inv']['datos'][f'{inv.pk}'] = inv.toJSON()
					item['inv']['lotes'].append({'id':inv.pk, 'text':f'{inv.lote} : {inv.stock}'})
				data.append(item)
		else:
			data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}

		# except Exception as e:
		# 	data['error'] = str(e)
		return JsonResponse(data, safe=False)
	
class ListadoEgreso(ValidarUsuario, ListView):
	permission_required = 'movimientos.view_egreso'
	context_object_name = 'egresos'
	template_name = 'pages/movimientos/egreso/listado_egresos.html'
	# permission_required = 'anuncios.requiere_secretria'
	model= Egreso
	ordering = ['-id']
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Listado de egresos"
		return context


class DetalleEgresoView(ValidarUsuario, DetailView):
	permission_required = 'movimientos.view_egreso'
	template_name = 'pages/movimientos/egreso/detalle_egreso.html'
	# permission_required = 'anuncios.requiere_secretria'
	model = Egreso
	context_object_name = 'egreso'
