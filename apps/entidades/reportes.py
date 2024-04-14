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
from django.db.models import Q

from .utils import link_callback
from .models import Perfil, Beneficiado
from .mixins import ValidarUsuario

class TodosPerfiles(View):
	# permission_required = 'anuncios.requiere_secretria'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	
	def get(self, request, *args, **kwargs):
		try:
			perfil = Perfil.objects.all().order_by('-id')
			formato_fecha = datetime.datetime.now().strftime("%d/%m/%Y")
			context = {
				'report_title': 'Listado de perfiles',
				'logo_img': '{}'.format('static/images/logo.jpg'),
				'user': f'{request.user.get_full_name()}',
				'perfil': perfil,
				'date': formato_fecha,
				'request':request,
			}
			template_path= get_template('reportes/todos_perfiles.html')
			html = template_path.render(context)
			response = HttpResponse(content_type='application/pdf')
			pisa.CreatePDF(html, dest=response, link_callback=link_callback)
			return response
		except Perfil.DoesNotExist:
			return redirect('vista')
		except Exception as e:
			return JsonResponse({'error': str(e)}, safe=False)

class TodosBeneficiados(View):
	# permission_required = 'anuncios.requiere_secretria'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	
	def get(self, request, *args, **kwargs):
		try:
			bene = Beneficiado.objects.all().order_by('-id')
			formato_fecha = datetime.datetime.now().strftime("%d/%m/%Y")
			context = {
				'report_title': 'Listado de Beneficiados',
				'logo_img': '{}'.format('static/images/logo.jpg'),
				'bene': bene,
				'date': formato_fecha,
				'request':request,
			}
			template_path= get_template('reportes/todos_beneficiados.html')
			html = template_path.render(context)
			response = HttpResponse(content_type='application/pdf')
			pisa.CreatePDF(html, dest=response, link_callback=link_callback)
			return response
		except Perfil.DoesNotExist:
			return redirect('vista')
		except Exception as e:
			return JsonResponse({'error': str(e)}, safe=False)