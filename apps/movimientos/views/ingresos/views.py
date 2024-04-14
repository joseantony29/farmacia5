
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
	CreateView,
	DetailView,
	View
)
from apps.entidades.mixins import ValidarUsuario, RedirectIfExistsContabilidadMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from ...forms import IngresoForm

from ...models import Ingreso, DetalleIngreso, TipoMov, Historial
from apps.inventario.models import Inventario, Producto
from apps.entidades.models import Perfil
# Create your views here.

class ListadoIngresos(ValidarUsuario, ListView):
	permission_required = 'movimientos.view_ingreso'
	context_object_name = 'ingresos'
	template_name = 'pages/movimientos/ingresos/listado_ingresos.html'
	# permission_required = 'anuncios.requiere_secretria'
	model= Ingreso
	ordering = ['-id']
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Listado de ingresos"
		return context

class DetalleIngresoView(ValidarUsuario, DetailView):
	permission_required = 'movimientos.view_ingreso'
	template_name = 'pages/movimientos/ingresos/detalle_ingreso.html'
	# permission_required = 'anuncios.requiere_secretria'
	model = Ingreso
	context_object_name = 'ingreso'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Detalles del ingreso"
		return context
	
class RegistrarIngreso(ValidarUsuario,RedirectIfExistsContabilidadMixin ,TemplateView):
	permission_required = 'movimientos.add_ingreso'
	redirect_url = '/listado-de-ingresos/'
	template_name = 'pages/movimientos/ingresos/registrar_ingreso.html'
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

				tipo_ingreso = TipoMov.objects.filter(pk=vents['tipo_ingreso']).first()
				ingreso = Ingreso()
				ingreso.fecha = vents['fecha']
				ingreso.descripcion = vents['descripcion']
				ingreso.tipo_ingreso = tipo_ingreso
				ingreso.save()

				for det in vents['det']:
					producto = Producto.objects.filter(pk=det['id']).first()
					inventario = Inventario()
					inventario.lote = det['lote']
					inventario.f_vencimiento = det['f_vencimiento']
					inventario.stock += det['cantidad'] 
					inventario.producto = producto
					inventario.save()

					detalle = DetalleIngreso()
					detalle.ingreso = ingreso
					detalle.inventario = inventario
					detalle.f_vencimiento = det['f_vencimiento']
					detalle.cantidad = det['cantidad']
					detalle.lote = det['lote']
					detalle.save()

					perfil = Perfil.objects.filter(usuario=request.user).first()
					movimiento = {
						'tipo_mov': tipo_ingreso,
						'perfil': perfil,
						'producto': inventario,
						'cantidad': det['cantidad']
					}
					Historial().crear_movimiento(movimiento)
					producto.contar_productos()

				messages.success(request,'Ingreso registrado correctamente')
				data['response'] = {'title': 'Exito!', 'data':'Compra registrada correctamente', 'type_response': 'success'}
		except Exception as e:
			data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Registrar ingreso"
		context["form"] = IngresoForm
		return context

class BuscarProductosIngresoView(ValidarUsuario, View):
	permission_required = 'entidades.ver_inicio'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		# try:
		action = request.POST['action']
		if action == 'search_productos':
			data = []
			productos = Producto.objects.filter(nombre__icontains=request.POST.get('term'))
			for i in productos[0:10]:
				item = i.toJSON()
				item['text'] = '{}'.format(i.nombre)
				item['id'] = i.pk
				data.append(item)

		elif action == 'search_productos_table':
			data = []
			productos = Producto.objects.all()
			for i in productos:
				item = i.toJSON()
				item['text'] = '{}'.format(i.nombre)
				item['id'] = i.pk
				data.append(item)
		else:
			data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}

		# except Exception as e:
		# 	data['error'] = str(e)
		return JsonResponse(data, safe=False)

class BuscarProductosView(ValidarUsuario, View):
	permission_required = 'entidades.ver_inicio'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		# try:
		action = request.POST['action']
		if action == 'search_productos':
			data = []
			ids_exclude = json.loads(request.POST.get('ids'))
			productos = Producto.objects.filter(nombre__icontains=request.POST.get('term'))
			for i in productos.exclude(pk__in=ids_exclude)[0:10]:
				item = i.toJSON()
				item['text'] = '{}'.format(i.nombre)
				item['tipo_insumo'] = i.tipo_insumo.nombre
				item['id'] = i.pk
				item['inv'] = []
				for inventario in Inventario.objects.filter(Q(comprometido__gt=0) | Q(stock__gt=0), producto_id=i.pk).order_by('f_vencimiento'):
					item['inv'].append(inventario.toJSON())
				data.append(item)

		elif action == 'search_productos_table':
			data = []
			ids_exclude = json.loads(request.POST.get('ids'))
			productos = Producto.objects.all()
			for i in productos.exclude(pk__in=ids_exclude):
				item = i.toJSON()
				item['text'] = '{}'.format(i.nombre)
				item['tipo_insumo'] = i.tipo_insumo.nombre
				item['id'] = i.pk
				item['inv'] = []
				for inventario in Inventario.objects.filter(Q(comprometido__gt=0) | Q(stock__gt=0), producto_id=i.pk).order_by('f_vencimiento'):
					item['inv'].append(inventario.toJSON()) 
				data.append(item)
		else:
			data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}

		# except Exception as e:
		# 	data['error'] = str(e)
		return JsonResponse(data, safe=False)