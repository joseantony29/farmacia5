from django.urls import path
from .views import (
    Inicio, 
    landing, 
    RegistrarPerfil, 
    ListadoPerfiles, 
    LoginPersonalidado, 
    ListaZona, 
    RegistrarZona, 
    ActualizarZona,
    Logout,
    CambiarClave,
    ActualizarLanding,
    ResetPassword,
    DetallesUsuario,
    EditarUsuario,
    ListadoMicomunidad,
    RegistrarComunidad,
    EditarComunidad,
    EliminarComunidad,
    MiPerfil, 
    ActualizarInfo,
    MenuReportes
)

from .reportes import (
    TodosPerfiles,
    TodosBeneficiados
)

urlpatterns = [
    path('inicio/', Inicio.as_view(), name='vista'),
    path('', landing.as_view()),
    path('actualizar-landing/', ActualizarLanding.as_view(), name='edit_landing'),
    path('menu-de-reportes/', MenuReportes.as_view(), name='reportes'),

    # perfil de usuario
    path('mi-perfil/', MiPerfil.as_view(), name='perfil'),
    path('actualizar-mi-informacion/', ActualizarInfo.as_view(), name='edit_info'),

    path('registrar-perfil/', RegistrarPerfil.as_view(), name='new_perfil'),
    path('listado-de-perfiles/', ListadoPerfiles.as_view(), name='lista_perfiles'),
    path('detalle-de-perfil/<int:pk>/', DetallesUsuario.as_view(), name='detalle_perfiles'),
    path('editar-perfil/<int:pk>/', EditarUsuario.as_view(), name='editar_perfil'),

    # mi comuniad    
    path('listado-de-mi-comunidad/', ListadoMicomunidad.as_view(), name='listado_mi_comunidad'),
    path('registrar-beneficiado-jornada/', RegistrarComunidad.as_view(), name='registrar_beneficiado_jornada'),
    path('editar-beneficiado/<int:pk>/', EditarComunidad.as_view(), name='editar_comunidad'),
    path('eliminar-beneficiado/<int:pk>/', EliminarComunidad.as_view(), name='eliminar_comunidad'),

    # control de acceso
    path('ingresar/', LoginPersonalidado.as_view(), name='login'),
    path('cerrar-sesion/', Logout.as_view(), name='logout'),
    path('actualizar-clave/', CambiarClave.as_view(), name='cambiar_clave'),
    path('reset-password/', ResetPassword.as_view(), name='reset_pass'),

    path('listado-de-zonas/', ListaZona.as_view(), name='lista_zonas'),
    path('registro-de-zona/', RegistrarZona.as_view(), name='nueva_zona'),
    path('actualizar-zona/', ActualizarZona.as_view(), name='actualizar_zona'),

    # reportes
    path('reportes/todos-los-perfiles/', TodosPerfiles.as_view(), name='t_perfiles'),
    path('reportes/todos-los-beneficiados/', TodosBeneficiados.as_view(), name='t_beneficiados'),
]
