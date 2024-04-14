from django import forms
from .models import Perfil, Zona, LandingPage, Comunidad, Beneficiado

class FormComunidad(forms.ModelForm):
	class Meta:
		model = Comunidad
		fields = '__all__'

class PerfilForm(forms.ModelForm):

	password1 = forms.CharField(label='Contrasena', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirme Contrasena', widget=forms.PasswordInput)
	email = forms.EmailField(label = 'Correo', widget=forms.EmailInput)
	codigo_tlf = forms.ChoiceField(choices=Perfil.CodigoTlf.choices)
	class Meta:
		model = Perfil
		fields = ['nacionalidad', 'cedula', 'nombres', 'apellidos', 'telefono', 'genero', 'f_nacimiento', 'embarazada', 'c_residencia', 'zona', 'direccion', 'rol', 'patologia']

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Las contrasena no coinciden")
		return password2

class ZonaForm(forms.ModelForm):
	class Meta:
		model = Zona
		fields = '__all__'

class FormLanding(forms.ModelForm):
	class Meta:
		model = LandingPage
		fields = '__all__'

class FormEditPerfil(forms.ModelForm):
	email = forms.EmailField(label = 'Correo', widget=forms.EmailInput)
	class Meta:
		model = Perfil
		fields = '__all__'
		exclude = ['nacionalidad', 'cedula', 'usuario']

class BeneficiadoForm(forms.ModelForm):
	class Meta:
		model = Beneficiado
		fields = '__all__'

