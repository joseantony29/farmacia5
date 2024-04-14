import subprocess
import sys
import io
import os

from django.views.generic import TemplateView, View
from django.http import JsonResponse, HttpResponse

from django.core import management
from django.contrib.auth import authenticate
from django.conf import settings
from datetime import datetime

from apps.entidades.mixins import ValidarUsuario

class DataBaseView(ValidarUsuario, TemplateView):
	template_name = 'db/database.html'
	permission_required = 'entidades.respaldar_db'

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			password = request.POST['password1']
			user = authenticate(request, username=request.user.username, password=password)
			if user is not None:
				data['response'] = {'title':'Exito!', 'data': 'Se ha descargado con exito', 'type_response': 'success'}
				data['redirect_url'] = '/respaldar-base-de-datos/'
			else:
				data['response'] = {'title':'Ocurrió un error!', 'data': 'CONTRASEÑA INCORRECTA', 'type_response': 'danger'}

		except Exception as e:
			print(e)
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['page_title'] = 'Copia de seguiridad de la base de datos'
		return context

class BackupDB(ValidarUsuario, View):
	permission_required = 'entidades.respaldar_db'

	def get(self, request, *args, **kwargs):
		try:
			# Capture standard output from 'dumpdata'
			sysout = sys.stdout
			buffer = io.StringIO()
			sys.stdout = buffer
			# Agrega los parámetros de exclusión aquí
			management.call_command('dumpdata', indent=4, exclude=['contenttypes', 'auth.Permission'])
			output = buffer.getvalue().encode('utf-8') # Byte-encoded output
			sys.stdout = sysout

			now = datetime.now()
			filename = f"backup_{now.strftime('%d%m%Y_%H%M%S')}.json"

			# HttpResponse with unencrypted output
			response = HttpResponse(output, content_type='application/json') # Change content_type
			response['Content-Disposition'] = f'attachment; filename={filename}' # Change file format to .json
			return response
		except Exception as e:
			return HttpResponse(f"An error occurred: {str(e)}")

class RestoreDBView(ValidarUsuario, TemplateView):
	template_name = 'db/restore_view.html'
	permission_required = 'entidades.recuperar_db'

	def post(self, request, *args, **kwargs):
		data = {}

		try:
			file_input = request.FILES['file_input']
			filename = file_input.name

			# Guarda el archivo recibido en el servidor
			with open(filename, 'wb+') as file:
				for chunk in file_input.chunks():
					file.write(chunk)

			# Usa el comando 'loaddata' para cargar los datos en la base de datos
			process = subprocess.Popen(['python', 'manage.py', 'loaddata', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			stdout, stderr = process.communicate()

			if len(stderr) > 0:
				data['response'] = {'title':'Ocurrió un error!', 'data': f"Error Inesperado:{stderr.decode(sys.getdefaultencoding(), errors='replace')}", 'type_response': 'danger'}
			else:
				os.remove(filename)
				data['response'] = {'title':'Exito!', 'data': 'Se ha cargado la base de datos con exito', 'type_response': 'success'}

		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['page_title'] = 'Restaurar base de datos'
		return context