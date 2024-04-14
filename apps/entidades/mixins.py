from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views import View

from apps.movimientos.models import ContabilidadFisica

class ValidarUsuario(LoginRequiredMixin, UserPassesTestMixin):
	permission_required = None
	redirect_url = '/inicio/'

	def test_func(self):
		return self.request.user.has_perm(self.permission_required)

	def handle_no_permission(self):
		if not self.request.user.has_perm(self.permission_required):
			messages.error(self.request, 'No tienes permisos para acceder a esta página.')
			return redirect(self.redirect_url)

		return super().handle_no_permission()

	def dispatch(self, request, *args, **kwargs):
		if not self.request.user.is_authenticated:
			return redirect('/ingresar/')
		return super().dispatch(request, *args, **kwargs)


class RedirectIfExistsContabilidadMixin(View):
	redirect_url = None # Define la URL a la que quieres redirigir

	def dispatch(self, request, *args, **kwargs):
		if self.redirect_url is None:
			raise NotImplementedError("Debes definir la URL de redirección en el mixin.")

		obj = ContabilidadFisica.objects.filter(estado__in=['PR','CO'])
		if obj:
			messages.error(request, 'No puede realizar esta accion porque hay un conteo de inventario fisico en proceso')
			return redirect(self.redirect_url)
		return super().dispatch(request, *args, **kwargs)