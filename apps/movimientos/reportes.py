from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.db.models import Q
from xhtml2pdf import pisa
import datetime
from datetime import date
from django.http import JsonResponse
from django.shortcuts import redirect

from apps.entidades.utils import link_callback
from .models import Jornada, Solicitud, DetalleIngreso, Ingreso, DetalleSolicitud ,Producto, Egreso, DetalleEgreso, Historial
from apps.entidades.mixins import ValidarUsuario

class TodasLasJornadas(View):
	# permission_required = 'anuncios.requiere_secretria'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	
	def get(self, request, pk, *args, **kwargs):
		try:
			jornada = Jornada.objects.filter(jefe_comunidad__zona = pk).order_by('-id')
			formato_fecha = datetime.datetime.now().strftime("%d/%m/%Y")
			context = {
				'report_title': 'Listado de Jornadas por zonas',
				'logo_img': '{}'.format('/home/joseantony29/farmacia4/static/images/logo.jpg'),
				'user': f'{request.user.get_full_name()}',
				'jornada': jornada,
				'date': formato_fecha,
				'request':request,
			}
			template_path= get_template('reportes/todas_jornadas.html')
			html = template_path.render(context)
			response = HttpResponse(content_type='application/pdf')
			pisa.CreatePDF(html, dest=response, link_callback=link_callback)
			return response
		except Jornada.DoesNotExist:
			return redirect('vista')
		except Exception as e:
			return JsonResponse({'error': str(e)}, safe=False)
		
class TodasLasJornadasFecha(View):
	# permission_required = 'anuncios.requiere_secretria'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	
	def get(self, request, fecha1, fecha2, *args, **kwargs):
		try:
			jornada = Jornada.objects.filter(fecha_solicitud__gte=fecha1, fecha_solicitud__lte=fecha2).order_by('-id')
			formato_fecha = datetime.datetime.now().strftime("%d/%m/%Y")
			context = {
				'report_title': f'Listado de solicitudes de jornadas desde: {fecha1} hasta: {fecha2}',
				'logo_img': '{}'.format('/home/joseantony29/farmacia4/static/images/logo.jpg'),
				'user': f'{request.user.get_full_name()}',
				'jornada': jornada,
				'date': formato_fecha,
				'request':request,
			}
			template_path= get_template('reportes/todas_jornadas_fecha.html')
			html = template_path.render(context)
			response = HttpResponse(content_type='application/pdf')
			pisa.CreatePDF(html, dest=response, link_callback=link_callback)
			return response
		except Jornada.DoesNotExist:
			return redirect('vista')
		except Exception as e:
			return JsonResponse({'error': str(e)}, safe=False)
		
class JornadasJefe(View):
	# permission_required = 'anuncios.requiere_secretria'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	
	def get(self, request, pk, *args, **kwargs):
		try:
			jornada = Jornada.objects.filter(jefe_comunidad__cedula = pk).order_by('-id')
			formato_fecha = datetime.datetime.now().strftime("%d/%m/%Y")
			context = {
				'report_title': 'Listado de Jornadas por jefe de comunidad',
				'logo_img': '{}'.format('/home/joseantony29/farmacia4/static/images/logo.jpg'),
				'user': f'{request.user.get_full_name()}',
				'jornada': jornada,
				'date': formato_fecha,
				'request':request,
			}
			template_path= get_template('reportes/jornada_jc.html')
			html = template_path.render(context)
			response = HttpResponse(content_type='application/pdf')
			pisa.CreatePDF(html, dest=response, link_callback=link_callback)
			return response
		except Jornada.DoesNotExist:
			return redirect('vista')
		except Exception as e:
			return JsonResponse({'error': str(e)}, safe=False)
		
class TodasLasSolicitudes(View):
	# permission_required = 'anuncios.requiere_secretria'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	
	def get(self, request, *args, **kwargs):
		try:
			solicitudes = Solicitud.objects.all().order_by('-id')
			formato_fecha = datetime.datetime.now().strftime("%d/%m/%Y")
			context = {
				'report_title': 'Listado de solicitudes',
				'logo_img': '{}'.format('/home/joseantony29/farmacia4/static/images/logo.jpg'),
				'user': f'{request.user.get_full_name()}',
				'solicitudes': solicitudes,
				'date': formato_fecha,
				'request':request,
			}
			template_path= get_template('reportes/todas_solicitudes.html')
			html = template_path.render(context)
			response = HttpResponse(content_type='application/pdf')
			pisa.CreatePDF(html, dest=response, link_callback=link_callback)
			return response
		except Solicitud.DoesNotExist:
			return redirect('vista')
		except Exception as e:
			return JsonResponse({'error': str(e)}, safe=False)
		
class TodasLasSolicitudesFecha(View):
	# permission_required = 'anuncios.requiere_secretria'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	
	def get(self, request, fecha1, fecha2, *args, **kwargs):
		try:
			solicitudes = Solicitud.objects.filter(fecha_soli__gte = fecha1, fecha_soli__lte=fecha2).order_by('-id')
			formato_fecha = datetime.datetime.now().strftime("%d/%m/%Y")
			context = {
				'report_title': f'Listado de solicitudes desde: {fecha1} hasta: {fecha2}',
				'logo_img': '{}'.format('/home/joseantony29/farmacia4/static/images/logo.jpg'),
				'user': f'{request.user.get_full_name()}',
				'solicitudes': solicitudes,
				'date': formato_fecha,
				'request':request,
			}
			template_path= get_template('reportes/todas_solicitudes_fecha.html')
			html = template_path.render(context)
			response = HttpResponse(content_type='application/pdf')
			pisa.CreatePDF(html, dest=response, link_callback=link_callback)
			return response
		except Solicitud.DoesNotExist:
			return redirect('vista')
		except Exception as e:
			return JsonResponse({'error': str(e)}, safe=False)
		
class SolicitudesEstado(View):
	# permission_required = 'anuncios.requiere_secretria'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	
	def get(self, request, est, *args, **kwargs):
		try:
			solicitudes = Solicitud.objects.filter(estado = est).order_by('-id')
			formato_fecha = datetime.datetime.now().strftime("%d/%m/%Y")
			context = {
				'est': est,
				'logo_img': '{}'.format('/home/joseantony29/farmacia4/static/images/logo.jpg'),
				'user': f'{request.user.get_full_name()}',
				'solicitudes': solicitudes,
				'date': formato_fecha,
				'request':request,
			}
			template_path= get_template('reportes/solicitud_estado.html')
			html = template_path.render(context)
			response = HttpResponse(content_type='application/pdf')
			pisa.CreatePDF(html, dest=response, link_callback=link_callback)
			return response
		except Solicitud.DoesNotExist:
			return redirect('vista')
		except Exception as e:
			return JsonResponse({'error': str(e)}, safe=False)
		
class ReportDetalleIngreso(View):
	# permission_required = 'anuncios.requiere_secretria'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	
	def get(self, request, pk, *args, **kwargs):
		try:
			ingreso = Ingreso.objects.get(id = DetalleIngreso.objects.get(id = pk).ingreso.pk)
			det_ingre = DetalleIngreso.objects.filter(ingreso__id = ingreso.pk )

			formato_fecha = datetime.datetime.now().strftime("%d/%m/%Y")
			context = {
				'report_title': 'Detalle de ingreso',
				'logo_img': '{}'.format('/home/joseantony29/farmacia4/static/images/logo.jpg'),
				'user': f'{request.user.get_full_name()}',
				'ingreso': ingreso,
				'detalle': det_ingre,
				'date': formato_fecha,
				'request':request,
			}
			template_path= get_template('reportes/det_ingreso.html')
			html = template_path.render(context)
			response = HttpResponse(content_type='application/pdf')
			pisa.CreatePDF(html, dest=response, link_callback=link_callback)
			return response
		except Solicitud.DoesNotExist:
			return redirect('vista')
		except Exception as e:
			return JsonResponse({'error': str(e)}, safe=False)
		
class ReportDetalleEgreso(View):
	# permission_required = 'anuncios.requiere_secretria'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	
	def get(self, request, pk, *args, **kwargs):
		try:
			egreso = Egreso.objects.get(id = DetalleEgreso.objects.get(id = pk).egreso.pk)
			det_egre = DetalleEgreso.objects.filter(egreso__id = egreso.pk )

			formato_fecha = datetime.datetime.now().strftime("%d/%m/%Y")
			context = {
				'report_title': 'Detalle de egreso',
				'logo_img': '{}'.format('/home/joseantony29/farmacia4/static/images/logo.jpg'),
				'user': f'{request.user.get_full_name()}',
				'egreso': egreso,
				'detalle': det_egre,
				'date': formato_fecha,
				'request':request,
			}
			template_path= get_template('reportes/det_egreso.html')
			html = template_path.render(context)
			response = HttpResponse(content_type='application/pdf')
			pisa.CreatePDF(html, dest=response, link_callback=link_callback)
			return response
		except Solicitud.DoesNotExist:
			return redirect('vista')
		except Exception as e:
			return JsonResponse({'error': str(e)}, safe=False)
		
class ReportDetalleSolicitud(View):
	# permission_required = 'anuncios.requiere_secretria'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	
	def get(self, request, pk, *args, **kwargs):
		try:
			solicitud = Solicitud.objects.get(id = pk)
			det_soli = DetalleSolicitud.objects.filter(solicitud = solicitud.id)

			formato_fecha = datetime.datetime.now().strftime("%d/%m/%Y")
			context = {
				'report_title': 'Detalle de solicitud',
				'logo_img': '{}'.format('/home/joseantony29/farmacia4/static/images/logo.jpg'),
				'user': f'{request.user.get_full_name()}',
				'solicitud': solicitud,
				'det': det_soli,
				'date': formato_fecha,
				'request':request,
			}
			template_path= get_template('reportes/det_solicitud.html')
			html = template_path.render(context)
			response = HttpResponse(content_type='application/pdf')
			pisa.CreatePDF(html, dest=response, link_callback=link_callback)
			return response
		except Solicitud.DoesNotExist:
			return redirect('vista')
		except Exception as e:
			return JsonResponse({'error': str(e)}, safe=False)
		
class ReporteInventarioFisico(View, ValidarUsuario):
	permission_required = 'movimientos.view_contabilidadfisica'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	
	def get(self, request, *args, **kwargs):
		try:
			productos = Producto.objects.filter(Q(comprometido__gt=0) | Q(total_stock__gt=0))
			formato_fecha = datetime.datetime.now().strftime("%d/%m/%Y")
			context = {
				'report_title': 'Inventario Fisico',
				'logo_img': '{}'.format('/home/joseantony29/farmacia4/static/images/logo.jpg'),
				'user': f'{request.user.get_full_name()}',
				'productos': productos,
				'date': formato_fecha,
				'request':request,
			}
			template_path= get_template('reportes/reporte_contabilidad_fisica.html')
			html = template_path.render(context)
			response = HttpResponse(content_type='application/pdf')
			pisa.CreatePDF(html, dest=response, link_callback=link_callback)
			return response
		except Producto.DoesNotExist:
			return redirect('vista')
		except Exception as e:
			return JsonResponse({'error': str(e)}, safe=False)
		
class HistorialMovimiento(View, ValidarUsuario):
	#permission_required = 'movimientos.view_contabilidadfisica'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	
	def get(self, request, *args, **kwargs):
		try:
			histo = Historial.objects.all()
			formato_fecha = datetime.datetime.now().strftime("%d/%m/%Y")
			context = {
				'report_title': 'Movimientos del inventario',
				'logo_img': '{}'.format('/home/joseantony29/farmacia4/static/images/logo.jpg'),
				'user': f'{request.user.get_full_name()}',
				'movi': histo,
				'date': formato_fecha,
				'request':request,
			}
			template_path= get_template('reportes/historial.html')
			html = template_path.render(context)
			response = HttpResponse(content_type='application/pdf')
			pisa.CreatePDF(html, dest=response, link_callback=link_callback)
			return response
		except Producto.DoesNotExist:
			return redirect('vista')
		except Exception as e:
			return JsonResponse({'error': str(e)}, safe=False)