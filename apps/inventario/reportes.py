from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.db.models import Q, F
from xhtml2pdf import pisa
import datetime
from datetime import date
from django.http import JsonResponse
from django.shortcuts import redirect
from django.db.models import Q

from apps.entidades.utils import link_callback
from .models import Inventario, Producto
from apps.entidades.mixins import ValidarUsuario

class TodosLosProductos(View):
	# permission_required = 'anuncios.requiere_secretria'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	
	def get(self, request, *args, **kwargs):
		try:
			prod = Inventario.objects.all().order_by('-id')
			formato_fecha = datetime.datetime.now().strftime("%d/%m/%Y")
			context = {
				'report_title': 'Listado de productos',
				'logo_img': '{}'.format('static/images/logo.jpg'),
				'user': f'{request.user.get_full_name()}',
				'prod': prod,
				'date': formato_fecha,
				'request':request,
			}
			template_path= get_template('reportes/todos_productos.html')
			html = template_path.render(context)
			response = HttpResponse(content_type='application/pdf')
			pisa.CreatePDF(html, dest=response, link_callback=link_callback)
			return response
		except Inventario.DoesNotExist:
			return redirect('vista')
		except Exception as e:
			return JsonResponse({'error': str(e)}, safe=False)
		
class ProductoStockMinimo(View):
	# permission_required = 'anuncios.requiere_secretria'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	
	def get(self, request, *args, **kwargs):
		try:
			productos_bajo_stock = Producto.objects.filter(total_stock__lt=F('stock_minimo'))
			formato_fecha = datetime.datetime.now().strftime("%d/%m/%Y")
			context = {
				'report_title': 'Listado de productos por debajo del stock minimo',
				'logo_img': '{}'.format('static/images/logo.jpg'),
				'user': f'{request.user.get_full_name()}',
				'prod': productos_bajo_stock,
				'date': formato_fecha,
				'request':request,
			}
			template_path= get_template('reportes/productos_stock_minimo.html')
			html = template_path.render(context)
			response = HttpResponse(content_type='application/pdf')
			pisa.CreatePDF(html, dest=response, link_callback=link_callback)
			return response
		except Inventario.DoesNotExist:
			return redirect('vista')
		except Exception as e:
			return JsonResponse({'error': str(e)}, safe=False)
