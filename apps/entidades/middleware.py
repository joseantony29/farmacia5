from django.http import HttpResponseRedirect
from django.utils import timezone
from django.template.loader import render_to_string
from apps.movimientos.email_utils import EmailThread
from django.db.models import Q

from apps.movimientos.models import Solicitud, DetalleSolicitud, DetalleIventarioSolicitud, TipoMov, Historial
from apps.inventario.models import Inventario, Producto
from apps.entidades.models import Perfil
from django.contrib.auth.models import User

class TemplateErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        for p in Producto.objects.filter(Q(comprometido__gt=0) | Q(total_stock__gt=0)):
            p.contar_productos()
        response = self.get_response(request)
        if response.status_code == 404:
            response = HttpResponseRedirect('/inicio/')
        return response

def check_solicitudes_en_espera(get_response):
    def middleware(request):
        # Verifica las solicitudes en espera de entrega que han estado en ese estado por más de 15 días
        hace_15_dias = timezone.now() - timezone.timedelta(days=15)
        solicitudes_en_espera = Solicitud.objects.filter(estado=Solicitud.Status.EN_ESPERA_DE_ENTREGA, fecha_en_espera__lte=hace_15_dias)

        for solicitud in solicitudes_en_espera:
            solicitud = Solicitud.objects.filter(pk=solicitud.pk).first()
            solicitud.estado = Solicitud.Status.PACIENTE_NO_RETIRO
            solicitud.proceso_actual = Solicitud.FaseProceso.FINALIZADO
            solicitud.save()

            usuario = User.objects.filter(username=f'{solicitud.perfil.nacionalidad}{solicitud.perfil.cedula}').first()
            # Cargar la plantilla HTML
            html_content = render_to_string('email/email_solicitud_sin_retirar.html', {'correo': usuario.email, 'nombres': usuario.perfil.nombres, 'apellidos':  usuario.perfil.apellidos})
            # Configurar el correo electrónico
            subject, from_email, to = 'SU SOLICITUD HA SIDO CANCELADA', 'FARMACIA COMUNITARIA ASIC LEONIDAS RAMOS', usuario.email
            text_content = 'Su solicitud ha sido cancelada por no retirar los medicamentos.'
            EmailThread(subject, text_content, from_email, [to], False, html_content).start()

            for det in DetalleSolicitud.objects.filter(solicitud_id=solicitud.pk):
                detproductos = DetalleIventarioSolicitud.objects.filter(detsolicitud=det)
                producto = Producto.objects.filter(pk=det.producto.pk).first()

                for d in detproductos:
                    inventario = Inventario.objects.filter(pk=d.inventario.pk).first()
                    inventario.comprometido -= d.cantidad
                    inventario.stock +=  d.cantidad
                    inventario.save()

                    perfil = Perfil.objects.filter(usuario=request.user).first()
                    tipo_ingreso, created = TipoMov.objects.get_or_create(nombre='PACIENTE NO RETIRO SOLICITUD DE MEDICAMENTOS', operacion='+')
                    movimiento = {
                        'tipo_mov': tipo_ingreso,
                        'perfil': perfil,
                        'producto': d.inventario,
                        'cantidad': d.cantidad
                    }
                    Historial().crear_movimiento(movimiento)
                producto.contar_productos()
        
        response = get_response(request)
        return response
    return middleware