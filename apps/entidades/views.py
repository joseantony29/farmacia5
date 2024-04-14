from django.shortcuts import render
from django.views.generic import TemplateView, View, DetailView, UpdateView, DeleteView
from django.contrib.auth.models import Permission
from .permisos import permisos_usuarios
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.template.loader import render_to_string
from apps.movimientos.email_utils import EmailThread
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .mixins import ValidarUsuario
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PerfilForm, ZonaForm, FormLanding, FormEditPerfil, FormComunidad, BeneficiadoForm

from apps.entidades.models import Perfil, User, Beneficiado, Zona, LandingPage, Comunidad

from apps.inventario.models import Producto
from apps.movimientos.models import Solicitud, Jornada
# Create your views here.

class Inicio(ValidarUsuario, TemplateView):
	permission_required = 'entidades.ver_inicio'
	template_name = 'pages/dashboard/inicio.html'

	def get(self, request, *args, **kwargs):
		context = {}

		cantidad_usuarios = Perfil.objects.all().count()
		cantidad_productos = Producto.objects.all().count()
		cantidad_solicitudes = Solicitud.objects.all().count()
		cantidad_jornadas = Jornada.objects.all().count()

		mis_solicitudes_de_medicamentos = Solicitud.objects.filter(perfil_id=request.user.perfil.pk).order_by('-pk')[:20]
		mis_solicitudes_de_jornadas_de_medicamentos = Jornada.objects.filter(jefe_comunidad_id=request.user.perfil.pk).order_by('-pk')[:20]


		context['cantidad_usuarios'] = cantidad_usuarios
		context['cantidad_productos'] = cantidad_productos
		context['cantidad_solicitudes'] = cantidad_solicitudes
		context['cantidad_jornadas'] = cantidad_jornadas
		context['mis_solicitudes_de_medicamentos'] = mis_solicitudes_de_medicamentos
		context['mis_solicitudes_de_jornadas_de_medicamentos'] = mis_solicitudes_de_jornadas_de_medicamentos

		return render(request, self.template_name, context)

class landing(TemplateView):
	template_name = 'landingPage/landing.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['landing'] = LandingPage().get_config()
		return context

class ActualizarLanding(ValidarUsuario, TemplateView):
	permission_required = 'entidades.change_landingpage'
	template_name = 'landingPage/edit_landing.html'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		action = request.POST['action']

		# Obtener la configuración de la página de inicio
		conf = LandingPage.get_config()

		if action == 'edit_landing':
			# Lista de nombres de campos para imágenes y texto
			campos = ['imagen1', 'imagen2', 'imagen3', 'imagen4', 'imagen5', 'texto1']

			# Iterar sobre los campos y actualizar el objeto conf si el campo está presente en request.FILES o request.POST
			for campo in campos:
				if campo.startswith('imagen'):
					if request.FILES.get(campo):
						setattr(conf, campo, request.FILES.get(campo))
				elif campo.startswith('texto'):
					if request.POST.get(campo):
						setattr(conf, campo, request.POST.get(campo))

			# Guardar el objeto actualizado
			conf.save()
			
			messages.add_message(request, messages.SUCCESS, 'La configuración de la página de inicio ha sido actualizada exitosamente.')
			return redirect(reverse_lazy('edit_landing'))

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = FormLanding(instance=LandingPage.get_config())
		return context
		
class ListadoPerfiles(ValidarUsuario, TemplateView):
	permission_required = 'entidades.view_perfil'
	template_name = 'pages/entidades/listado_usuarios.html'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']

			if action == 'search_usuarios':
				data = []
				for i in Perfil.objects.filter(rol = request.POST['filter_id']):
					item = i.toJSON()
					data.append(item)
				# Convertir la lista de datos en un JsonResponse
				return JsonResponse(data, safe=False)
				
		except Exception as e:
			data['error'] = str(e) # Ahora esto es válido porque data es un diccionario
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sub_title'] = 'Lista de Usuarios'
		context['form'] = PerfilForm()
		return context

class RegistrarPerfil(LoginRequiredMixin, View):

	def post(self, request, *args, **kwargs):
		data = {}
		action = request.POST['action']
		
		if action == 'nuevo_usuario':
			username = f'{request.POST["nacionalidad"]}{request.POST["cedula"]}'
			if not User.objects.filter(username=username).exists() and not Perfil.objects.filter(cedula = request.POST["cedula"]):
				usuario = User()
				usuario.username = username
				usuario.first_name = request.POST["nombres"]
				usuario.last_name = request.POST["apellidos"]
				usuario.email = request.POST["email"]
				usuario.is_active = request.POST.get('is_active', False)
				usuario.set_password(request.POST["password1"])
				usuario.save()

				permissions = Permission.objects.filter(codename__in=permisos_usuarios[request.POST["rol"]])
				usuario.user_permissions.set(permissions)
				usuario.save()

				if request.POST["genero"] == 'MA':
					embarazada = False
				else:
					embarazada = request.POST["embarazada"]
				
				perfil = Perfil.objects.create(
					nacionalidad=request.POST["nacionalidad"],
					cedula=request.POST["cedula"],
					nombres=request.POST["nombres"],
					apellidos=request.POST["apellidos"],
					telefono=f'{request.POST["codigo_tlf"]}{request.POST["telefono"]}',
					genero=request.POST["genero"],
					embarazada=embarazada, # Usa el valor calculado aquí
					f_nacimiento=request.POST["f_nacimiento"],
					c_residencia=request.FILES.get("c_residencia"),
					zona=Zona.objects.get(id=request.POST["zona"]),
					direccion=request.POST["direccion"],
					patologia=request.POST["patologia"],
					rol=request.POST["rol"],
					usuario=usuario
				)

				if Beneficiado.objects.filter(cedula=perfil.cedula).first():
					beneficiado = Beneficiado.objects.filter(cedula=perfil.cedula).first()
				else:
					beneficiado = Beneficiado()
				beneficiado.perfil_id = perfil.pk
				beneficiado.nacionalidad = request.POST["nacionalidad"]
				beneficiado.cedula = request.POST["cedula"]
				beneficiado.nombres = request.POST["nombres"]
				beneficiado.apellidos = request.POST["apellidos"]
				beneficiado.telefono = f'{request.POST["codigo_tlf"]}{request.POST["telefono"]}'
				beneficiado.genero = request.POST["genero"]
				beneficiado.f_nacimiento = request.POST["f_nacimiento"]
				beneficiado.patologia = request.POST["patologia"]
				if request.POST["genero"] == 'MA':
					beneficiado.embarazada = False
				else:
					beneficiado.embarazada = request.POST["embarazada"]
				if request.FILES.get("c_residencia"):
					beneficiado.c_residencia = request.FILES.get("c_residencia")
				beneficiado.zona_id = request.POST["zona"]
				beneficiado.direccion = request.POST["direccion"]
				beneficiado.save()

				# enviando el correo de registro

				# Cargar la plantilla HTML
				html_content = render_to_string('email/email_registro.html', {'correo': request.POST['email'],'user': f'{request.POST["nacionalidad"]}{request.POST["cedula"]}','nombres': request.POST['nombres'], 'apellidos': request.POST['apellidos']})
				# Configurar el correo electrónico
				subject, from_email, to = 'REGISTRO EXITOSO', 'FARMACIA COMUNITARIA ASIC LEONIDAS RAMOS', request.POST['email']
				text_content = 'ESTE ES UN MENSAJE DE BIENVENIDA.'
				EmailThread(subject, text_content, from_email, [to], False, html_content).start()
				
				data['response'] = {'title': 'Exito!', 'data': 'Usuario creado correctamente.', 'type_response': 'success'}

			else:
				data['response'] = {'title': 'Ocurrió un error!', 'data': 'Usuario ya esta registrado.', 'type_response': 'danger'}
		else:
			data['response'] = {'title': 'Ocurrió un error!', 'data': 'Error de solicitud.', 'type_response': 'danger'}
				
		
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = PerfilForm()
		return context

class DetallesUsuario(DetailView):
	template_name = template_name = 'pages/entidades/detalle_usuario.html'
	model = Perfil
	
	def get(self, request, pk, *args, **kwargs):

		perfil = Perfil.objects.get(pk = pk)
		beneficiados = Beneficiado.objects.filter(perfil__cedula = perfil.cedula)

		
		return render(request, self.template_name, {'perfil': perfil, 'beneficiado': beneficiados})

class EditarUsuario(SuccessMessageMixin, UpdateView):
	model = Perfil
	form_class = FormEditPerfil
	success_message = 'Perfil editado correctamente'
	template_name = 'pages/entidades/editar_usuarios.html'
	success_url = reverse_lazy('lista_perfiles')

	def get_initial(self):
		initial = super().get_initial()
		perfil = Perfil.objects.get(id = self.object.pk)
		user = User.objects.get(username = f'{perfil.nacionalidad}{perfil.cedula}')
		# Aquí puedes agregar los datos iniciales para tus campos de formulario.
		# Por ejemplo, si tienes un campo llamado 'nombre' en tu formulario, puedes hacer:
		initial['email'] = user.email
		return initial

	def form_valid(self, form):

		perfil = Perfil.objects.get(id = self.object.pk)
		user = User.objects.get(username = f'{perfil.nacionalidad}{perfil.cedula}')

		self.object = form.save()

		user.first_name = form.cleaned_data['nombres']
		user.last_name = form.cleaned_data['apellidos']
		user.user_permissions.clear()
		user.email = form.cleaned_data['email']
		permissions = Permission.objects.filter(codename__in=permisos_usuarios[form.cleaned_data['rol']])
		user.user_permissions.set(permissions)
		user.save()

		bene = Beneficiado.objects.get(id = self.object.pk)
		bene.nombres = form.cleaned_data['nombres']
		bene.apellidos = form.cleaned_data['apellidos']
		bene.genero = form.cleaned_data['genero']
		bene.f_nacimiento = form.cleaned_data['f_nacimiento']
		bene.embarazada = form.cleaned_data['embarazada']
		bene.telefono = form.cleaned_data['telefono']
		bene.zona = form.cleaned_data['zona']
		bene.c_residencia = form.cleaned_data['c_residencia']
		bene.direccion = form.cleaned_data['direccion']
		bene.patologia = form.cleaned_data['patologia']
		bene.save()

		return super().form_valid(form)

class ListadoMicomunidad(ValidarUsuario, TemplateView):
	permission_required = 'entidades.view_comunidad'
	template_name = 'pages/mi_comunidad/listado_mi_comunidad.html'
	
	def get(self, request, *args, **kwargs):
		perfil = Perfil.objects.filter(usuario = request.user).first()
		if perfil:
			mi_comunidad = Comunidad.objects.filter(jefe_comunidad = perfil)
		return render(request, self.template_name, {'mi_comunidad': mi_comunidad, 'sub_title':'Listado de mi comunidad'})

class RegistrarComunidad(ValidarUsuario, TemplateView):
	permission_required = 'entidades.add_comunidad'
	template_name = 'pages/mi_comunidad/registrar_beneficiado.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Registrar Beneficiado"
		context["form"] = FormComunidad(self.request.POST or None)
		return context

	def post(self, request, *args, **kwargs):
		try:
			comunidad = Comunidad.objects.filter(cedula=request.POST.get('cedula')).first()
			perfil = Perfil.objects.filter(usuario=request.user).first()
			if not comunidad:
				comunidad = Comunidad()
				comunidad.nacionalidad = request.POST.get('nacionalidad')
				comunidad.cedula = request.POST.get('cedula')
				comunidad.nombres = request.POST.get('nombres')
				comunidad.apellidos = request.POST.get('apellidos')
				comunidad.genero = request.POST.get('genero')
				comunidad.patologia = request.POST.get('patologia')
				comunidad.jefe_comunidad_id = perfil.pk
				comunidad.save()
				messages.success(request, 'Se ha registrado correctamente.')
			else:
				messages.error(request, 'Este beneficiado ya existe.')
				return render(request, self.template_name, self.get_context_data(**kwargs))
		except Exception as e:
			messages.error(request, 'Ocurrió un error al procesar la solicitud.')
		return redirect('listado_mi_comunidad')

class EditarComunidad(ValidarUsuario, UpdateView):
	permission_required = 'entidades.change_comunidad'
	template_name = 'pages/mi_comunidad/editar_comunidad.html'
	model = Comunidad
	form_class = FormComunidad

	def get_success_url(self):
		return reverse('listado_mi_comunidad')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Editar Comunidad"
		return context

	def form_valid(self, form):
		# Validación de que la cédula no existe
		cedula = form.cleaned_data.get('cedula')
		if Comunidad.objects.filter(cedula=cedula).exclude(pk=self.object.pk).exists():
			messages.error(self.request, 'La cédula ya existe.')
			return self.form_invalid(form)
		
		# Asignación de jefe_comunidad
		perfil = Perfil.objects.filter(usuario=self.request.user).first()
		if perfil:
			form.instance.jefe_comunidad = perfil
		else:
			messages.error(self.request, 'El perfil del usuario no existe.')
			return self.form_invalid(form)
		messages.success(self.request, 'El beneficiado ha sido actualizado correctamente.')
		return super().form_valid(form)

class EliminarComunidad(ValidarUsuario, View):
	permission_required = 'entidades.delete_comunidad'
	
	def get(self, request, pk):
		comunidad = Comunidad.objects.filter(pk=pk).first()
		# Verificar si la comunidad está relacionada con alguna jornada
		if Jornada.objects.filter(comunidad=comunidad).exists():
			messages.error(request, 'No se puede eliminar el beneficiado porque está relacionada con una jornada.')
			return redirect('listado_mi_comunidad')
		else:
			# Si no hay jornadas relacionadas, proceder con la eliminación
			comunidad.delete()
			messages.success(request, 'El beneficiado ha sido eliminado correctamente.')
		return redirect('listado_mi_comunidad')

# control de acceso	
class LoginPersonalidado(TemplateView):
	template_name = 'acceso/login.html'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action_login']

			if action == 'login':
				naci = request.POST['naci']
				ci = request.POST['ci']
				username = f'{naci}{ci}'
				password = request.POST['password']

				user = authenticate(request, username=username, password=password)
				if user is not None:
					login(request, user)
					data['response'] = {'title':'Exito!', 'data': 'Ingreso validado correctamente.', 'type_response': 'success'}

				else:
					if not User.objects.filter(username = username):
						data['response'] = {'title':'Ocurrió un error!', 'data': 'El usuario no existe.', 'type_response': 'danger'}
					else:
						data['response'] = {'title':'Ocurrió un error!', 'data': 'Contraseña incorrecta o usuario inactivo', 'type_response': 'danger'}

		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

class CambiarClave(LoginRequiredMixin, View):
	# permission_required = 'core.change_password_users'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		action = request.POST['action_password']
		try:
			
			if action == 'cambiar_clave':

				username = request.POST['username']
				password = request.POST['password_actual']

				user = authenticate(request, username=username, password=password)
				if user is not None:
					usuario = User.objects.get(username = username)
					usuario.set_password(request.POST['new_password'])
					usuario.save()
					logout(request)
					data['response'] = {'title':'Exito!', 'data': 'Contraseña actualizada correctamente.', 'type_response': 'success'}
				
				else:
					data['response'] = {'title':'Ocurrió un error!', 'data': 'Contraseña actual incorrecta.', 'type_response': 'danger'}
			else:
				data['response'] = {'title':'Ocurrió un error!', 'data': 'Solicitud invalida.', 'type_response': 'danger'}
					
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

class ResetPassword(LoginRequiredMixin, View):
	#permission_required = 'core.change_password_users'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		action = request.POST['action_reset']
		try:
			
			if action == 'reset_password':

				username = request.POST['username_reset']
				password = request.POST['password1_reset']

				usuario = User.objects.get(username = username)
				usuario.set_password(password)
				usuario.save()
				data['response'] = {'title':'Exito!', 'data': 'Contraseña actualizada correctamente.', 'type_response': 'success'}
			else:
				data['response'] = {'title':'Ocurrió un error!', 'data': 'Solicitud invalida.', 'type_response': 'danger'}
					
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

class Logout(View):
	def get(self, request):
		logout(request)
		return redirect('/')

class ListaZona(ValidarUsuario, TemplateView):
	permission_required = 'entidades.view_zona'
	template_name = "pages/mantenimiento/listado_zonas.html"

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']

			if action == 'search_zonas':
				data = []
				for i in Zona.objects.all():
					item = i.toJSON()
					data.append(item)
				# Convertir la lista de datos en un JsonResponse
				return JsonResponse(data, safe=False)
				
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Listado de zonas"
		return context

class RegistrarZona(LoginRequiredMixin,View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']

			if action == 'nueva_zona':
				form = ZonaForm(request.POST)

				if form.is_valid():
					form.save()
					data['response'] = {'title':'Exito!', 'data': 'Zona registrada correctamente.', 'type_response': 'success'}
				else:
					data['response'] = {'title':'Ocurrió un error!', 'data': 'Ocurrió un error inesperado.', 'type_response': 'danger'}

		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)
	
class ActualizarZona(LoginRequiredMixin, View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		action = request.POST['action']
		try:
			if action == 'edit_zona':
				zona = Zona.objects.filter(id = request.POST['id']).first()
				form = ZonaForm(request.POST, instance=zona)

				if form.is_valid():
					form.save()
					data['response'] = {'title':'Exito!', 'data': 'La zona se ha actualizado correctamente.', 'type_response': 'success'}
				else:
					data['response'] = {'title':'Ocurrió un error!', 'data': 'Ocurrió un error inesperado.', 'type_response': 'danger'}
			
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)	

class ActualizarInfo(LoginRequiredMixin, View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		action = request.POST['action_edit']
		
		if action == 'editar_info':
			perfil = Perfil.objects.get(usuario__username = self.request.user.username)
			user = User.objects.get(username = self.request.user.username)
			user.email = request.POST['email']
			user.save()

			perfil.telefono = request.POST['telefono']
			if request.POST.get('embarazada') == 'on':
				perfil.embarazada = True
			else:
				perfil.embarazada = False
			perfil.zona = Zona.objects.get(zona_residencia = request.POST['zona'])
			if request.FILES.get("c_residencia"):
				perfil.c_residencia = request.FILES.get("c_residencia")
			perfil.direccion = request.POST['direccion']
			perfil.patologia = request.POST['patologia']
			perfil.save()

			data['response'] = {'title':'Exito!', 'data': 'Perfil actualizado correctamente.', 'type_response': 'success'}

		else:
			data['response'] = {'title':'Ocurrió un error!', 'data': 'Ocurrió un error inesperado.', 'type_response': 'danger'}
	

		return JsonResponse(data, safe=False)	
	
# PERFIL DE USUARIO
	
class MiPerfil(TemplateView):
	template_name = 'acceso/perfil.html'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		
		action = request.POST['action']

		if action == 'search_beneficiados':
			user = User.objects.get(username = self.request.user.username)
			perfil = Perfil.objects.get(usuario = user)
			data = []
			for i in Beneficiado.objects.filter(perfil = perfil).exclude(cedula=perfil.cedula):
				item = i.toJSON()
				data.append(item)
			# Convertir la lista de datos en un JsonResponse
			return JsonResponse(data, safe=False)

		if action == 'nuevo_bene':
			
			bene = Beneficiado()
			if not Beneficiado.objects.filter(cedula = request.POST['cedula']).exists():
				bene.perfil = Perfil.objects.get(usuario__username = self.request.user.username ) 
				bene.nacionalidad = request.POST['nacionalidad']
				bene.cedula = request.POST['cedula']
				bene.nombres = request.POST['nombres']
				bene.apellidos = request.POST['apellidos']
				bene.f_nacimiento = request.POST['f_nacimiento']
				bene.telefono = request.POST['telefono']
				bene.genero = request.POST['genero']
				bene.parentesco = request.POST['parentesco']
				if request.POST.get('embarazada') == 'on':
					bene.embarazada = True
				else:
					bene.embarazada = False
				bene.zona = Zona.objects.get(id = request.POST['zona'] ) 
				if request.FILES.get("c_residencia"):
					bene.c_residencia = request.FILES.get("c_residencia")
				bene.direccion = request.POST['direccion']
				bene.patologia = request.POST['patologia']
				bene.rol = 'PA'
				bene.save()
				data['response'] = {'title':'Exito!', 'data': 'Beneficiado registrado correctamente.', 'type_response': 'success'}
					
			else:
				data['response'] = {'title':'Ocurrió un error!', 'data': 'Beneficiado ya se encuentra registrado.', 'type_response': 'danger'}

		if action == 'editar_bene':

			beneficiado = Beneficiado.objects.get(cedula = request.POST.get('id'))
			beneficiado.telefono = request.POST['telefono_bene']
			beneficiado.zona = Zona.objects.get(id = int(request.POST.get('zona_bene')))
			beneficiado.parentesco = request.POST['parentesco']
			if request.POST.get('embarazada_bene') == 'on':
				beneficiado.embarazada = True
			else:
				beneficiado.embarazada = False
			if request.FILES.get("c_residencia_bene"):
				beneficiado.c_residencia = request.FILES.get("c_residencia_bene")
			beneficiado.direccion = request.POST['direccion_bene']
			beneficiado.patologia = request.POST['patologia_bene']
			beneficiado.save()

			data['response'] = {'title':'Exito!', 'data': 'Beneficiado registrado correctamente.', 'type_response': 'success'}
		
		return JsonResponse(data, safe=False)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = User.objects.get(username = self.request.user.username)
		perfil = Perfil.objects.get(usuario = user)
		beneficiados = Beneficiado.objects.filter(perfil = perfil)
		# Aquí puedes agregar cualquier dato que desees pasar a la plantilla
		context['mi_dato'] = perfil
		context['zonas'] = Zona.objects.all()
		context['bene'] = beneficiados
		context['form'] = BeneficiadoForm()
		return context
	
class MenuReportes(TemplateView):
	template_name = 'reportes/menu_reportes.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['zonas'] = Zona.objects.all()
		context['j_c'] = Perfil.objects.filter(rol = 'JC')
		return context
