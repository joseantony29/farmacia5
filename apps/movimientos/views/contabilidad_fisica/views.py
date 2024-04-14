import json
from datetime import date, datetime

from apps.entidades.mixins import ValidarUsuario
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic import (
	TemplateView,
	UpdateView,
	DetailView,
	View
)

from apps.movimientos.models import ContabilidadFisica, DetContabilidadFisica, InventarioContFisica, TipoMov, Historial
from apps.inventario.models import Producto, Inventario
from apps.entidades.models import Perfil
from django.contrib.auth.models import User

from apps.movimientos.forms import ContabilidadForm

class ListadoContabilidadFisica(ValidarUsuario, TemplateView):
	permission_required = 'movimientos.view_contabilidadfisica'
	template_name = 'pages/contabilidad_fisica/listado_contabilidad_fisica.html'
	# permission_required = 'anuncios.requiere_secretria'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		contabilidades_fisicas = ContabilidadFisica.objects.all().order_by('-pk')
		context["sub_title"] = "Listado de ajuste de inventario fisico"	
		context['contabilidades_fisicas'] = contabilidades_fisicas
		return context

class DetalleContabilidadFisica(ValidarUsuario, TemplateView):
	permission_required = 'movimientos.view_contabilidadfisica'
	template_name = 'pages/contabilidad_fisica/detalle_contabilidad_fisica.html'
	# permission_required = 'anuncios.requiere_secretria'

	def get(self, request, pk, *args, **kwargs):
		context = {}
		try:
			contabilidad = ContabilidadFisica.objects.get(pk=pk)
			context['contabilidad'] = contabilidad
			context["sub_title"] = "Detalle de Inventario fisico"
			return render(request, self.template_name, context)
		except ContabilidadFisica.DoesNotExist:
			return redirect('listado_contabilidad_fisica')
	
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = []
		# try:
		with transaction.atomic():
			pk = request.POST.get('pk')
			for i in InventarioContFisica.objects.filter(detcontabilidad_id=pk):
				item = i.toJSON()
				data.append(item)
		# except Exception as e:
		# 	data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}
		# 	data['error'] = str(e)
		return JsonResponse(data, safe=False)

class RegistrarContabilidadFisica(ValidarUsuario, TemplateView):
	permission_required = 'movimientos.add_contabilidadfisica'
	template_name = 'pages/contabilidad_fisica/registrar_contabilidad_fisica.html'
	object = None

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		# try:
		with transaction.atomic():
			vents = json.loads(request.POST['vents'])
			contabilidad = ContabilidadFisica()
			contabilidad.proceso_actual = ContabilidadFisica.FaseProceso.ALMACENISTA
			contabilidad.estado = ContabilidadFisica.Status.EN_PROCRESO 
			contabilidad.save()

			for det in vents['det']:
				producto = Producto.objects.filter(pk=det['id']).first()

				detalle = DetContabilidadFisica()
				detalle.contabilidad_id = contabilidad.pk
				detalle.producto_id = producto.pk
				detalle.cantidad_contada = det['cantidad']
				detalle.cantidad_inventario = producto.total_stock
				detalle.save()

				for inv in det['inv']:
					det_inv = InventarioContFisica()
					det_inv.detcontabilidad_id = detalle.pk
					det_inv.inventario_id = inv['id']
					det_inv.cantidad_contada = inv['cantidad_contada']
					det_inv.cantidad_inventario = inv['stock']
					det_inv.save()

			messages.success(request,'Ajuste de inventario fisico registrado correctamente')
			data['response'] = {'title':'Exito!', 'data': 'Ajuste de inventario fisico registrado correctamente', 'type_response': 'success'}
		# except Exception as e:
		# 	data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}
		# 	data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Registrar Inventario fisico"
		# context["form"] = ContabilidadForm()
		return context

class EditarContabilidadFisica(ValidarUsuario, SuccessMessageMixin, UpdateView):
	permission_required = 'movimientos.change_contabilidadfisica'
	template_name = 'pages/contabilidad_fisica/modificar_contabilidad_fisica.html'
	model = ContabilidadFisica
	form_class = ContabilidadForm
	success_massage = 'El Inventario fisico ha sido modificada correctamente'
	object = None

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		if request.user.perfil.rol == 'AD':
			if self.get_object().estado in ['PR','RE','AP']:
				return redirect('listado_contabilidad_fisica')
		if request.user.perfil.rol == "AL":
			if self.get_object().estado in ['AP','RE','CO']:
				return redirect('listado_contabilidad_fisica')
		return super().dispatch(request, *args, **kwargs)
		
	def post(self, request, *args, **kwargs):
		data = {}
		# try:
		with transaction.atomic():
			vents = json.loads(request.POST['vents'])

			contabilidad = self.get_object()
			contabilidad.estado = vents['estado']

			if vents['estado'] == 'AP':
				contabilidad.proceso_actual = ContabilidadFisica.FaseProceso.FINALIZADO
			elif vents['estado'] == 'CO':
				contabilidad.proceso_actual = ContabilidadFisica.FaseProceso.ADMINISTRADOR
			elif vents['estado'] == 'RE':
				contabilidad.motivo_rechazo = vents['motivo_rechazo']
				contabilidad.proceso_actual = ContabilidadFisica.FaseProceso.FINALIZADO
			contabilidad.save()

			InventarioContFisica.objects.filter(detcontabilidad__contabilidad=self.get_object()).delete()
			DetContabilidadFisica.objects.filter(contabilidad=self.get_object()).delete()

			for det in vents['det']:
				producto = Producto.objects.filter(pk=det['producto']).first()

				detalle = DetContabilidadFisica() 
				detalle.contabilidad = contabilidad
				detalle.producto_id = producto.pk
				detalle.cantidad_contada = det['cantidad_contada']
				detalle.cantidad_inventario = det['cantidad_inventario']
				detalle.save()

				for inv in det['inv']:
					det_inv = InventarioContFisica()
					det_inv.detcontabilidad_id = detalle.pk
					det_inv.inventario_id = inv['inventario']
					det_inv.cantidad_contada = inv['cantidad_contada']
					det_inv.cantidad_inventario = inv['cantidad_inventario']
					det_inv.save()

				if vents['estado'] == 'AP':
					# CODIGO QUE DEBES COLOCAR PHIND						
					for inv in det['inv']:
						inventario = Inventario.objects.filter(pk=inv['inventario']).first()
						inventario.stock = inv['cantidad_contada']
						inventario.save()

						diferencia = inv['cantidad_contada'] - inv['cantidad_inventario']

						perfil = Perfil.objects.filter(usuario=self.request.user).first()
						movimiento = {
							'tipo_mov': '',
							'perfil': perfil,
							'producto': inventario,
							'cantidad': 0
						}

						if diferencia > 0:
							tipo_ingreso, created = TipoMov.objects.get_or_create(nombre='AJUSTE INVENTARIO FISICO (SUMA)', operacion='+')
							movimiento['tipo_mov'] = tipo_ingreso
							movimiento['cantidad'] = diferencia
						elif diferencia < 0:
							tipo_ingreso, created = TipoMov.objects.get_or_create(nombre='AJUSTE INVENTARIO FISICO (RESTA)', operacion='-')
							movimiento['tipo_mov'] = tipo_ingreso
							movimiento['cantidad'] = abs(diferencia)
						elif diferencia == 0:
							tipo_ingreso, created = TipoMov.objects.get_or_create(nombre='AJUSTE INVENTARIO FISICO (IGUAL)', operacion='=')
							movimiento['tipo_mov'] = tipo_ingreso
							movimiento['cantidad'] = diferencia
						Historial().crear_movimiento(movimiento)

					producto.contar_productos()

			messages.success(request,'Ajuste de inventario fisico registrado correctamente')
			data['response'] = {'title':'Exito!', 'data': 'Ajuste de inventario fisico registrado correctamente', 'type_response': 'success'}
		# except Exception as e:
		# 	data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}
		# 	data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_detail(self):
		data = []
		try:
			for i in DetContabilidadFisica.objects.filter(contabilidad_id=self.get_object().id):
				item = i.toJSON()
				item['tipo_insumo'] = i.producto.tipo_insumo.nombre
				item['nombre'] = i.producto.nombre
				item['id'] = i.pk
				item['inv'] = []
				for inventario in InventarioContFisica.objects.filter(detcontabilidad_id=i.pk):
					item['inv'].append(inventario.toJSON())
				data.append(item)
		except:
			pass
		return data

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['rol'] = self.request.user.perfil.rol
		context["sub_title"] = "Modificar Inventario fisico"
		context['det'] = json.dumps(self.get_detail(),  sort_keys=True,indent=1, cls=DjangoJSONEncoder)
		return context

class RechazarContabilidadFisica(ValidarUsuario, SuccessMessageMixin, View):
	permission_required = 'movimientos.change_contabilidadfisica'
	success_massage = 'El ajuste de inventario fisico ha sido rechazada'
	# permission_required = 'anuncios.requiere_secretria'
	object = None
		
	def post(self, request, *args, **kwargs):
		try:
			with transaction.atomic():
				motivo_del_rechazo = request.POST.get('motivo_rechazo')
				pk = request.POST.get('pk')
				contabilidad = ContabilidadFisica.objects.filter(pk=pk).first()
				if contabilidad:
					if request.user.perfil.rol == 'AD':
						if contabilidad.estado in ['PR', 'CO']:
							contabilidad.estado = ContabilidadFisica.Status.RECHAZADO
							contabilidad.proceso_actual = ContabilidadFisica.FaseProceso.FINALIZADO
							contabilidad.motivo_rechazo = motivo_del_rechazo
							contabilidad.save()
			
							messages.success(request, self.success_massage)
						else:
							messages.error(request, 'El ajuste de inventario fisico debe estar en proceso o contabilizado para realizar esta accion.')
					else:
						messages.error(request, 'No tienes permisos para realizar esta acción.')
				else:
					messages.error(request, 'El ajuste de inventario fisico no existe.')
		except Exception as e:
			messages.error(request, 'Ocurrió un error al procesar la jornada.')
		return redirect('listado_contabilidad_fisica')

class BuscarProductosValidadosView(ValidarUsuario, View):
	permission_required = 'entidades.ver_inicio'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		# try:
		action = request.POST['action']
		if action == 'cargar_productos':
			data = []
			productos = Producto.objects.filter(Q(comprometido__gt=0) | Q(total_stock__gt=0))
			for i in productos:
				item = i.toJSON()
				item['text'] = '{}'.format(i.nombre)
				item['tipo_insumo'] = i.tipo_insumo.nombre
				item['id'] = i.pk
				item['cantidad'] = 0
				item['inv'] = []
				for inventario in Inventario.objects.filter(Q(comprometido__gt=0) | Q(stock__gt=0), producto_id=i.pk).order_by('f_vencimiento'):
					item['inv'].append(inventario.toJSON())
				data.append(item)
		else:
			data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}

		# except Exception as e:
		# 	data['error'] = str(e)
		return JsonResponse(data, safe=False)