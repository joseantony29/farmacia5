from django.contrib import admin
from .models import (
    Solicitud, 
    DetalleSolicitud, 
    Jornada, 
    DetalleJornada, 
    Ingreso, 
    DetalleIngreso, 
    TipoMov, 
    Historial, 
    DetalleIventarioSolicitud, 
    DetalleIventarioJornada,
    ContabilidadFisica,
    DetContabilidadFisica,
    InventarioContFisica,
    Egreso,
    DetalleEgreso
)
# Register your models here.

class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('pk', 'fecha_soli', 'proceso_actual', 'estado', 'tipo_solicitud')
    list_filter = ('proceso_actual', 'estado', 'tipo_solicitud')
    search_fields = ('pk', 'proceso_actual', 'estado', 'tipo_solicitud')
    ordering = ('pk', 'fecha_soli')
    # readonly_fields = ('date_of_birth',)

class DetSolicitudAdmin(admin.ModelAdmin):
    list_display = ('pk', 'solicitud', 'producto', 'cant_solicitada', 'cant_entregada')
    list_filter = ('producto',)
    search_fields = ('pk', 'producto')
    ordering = ('pk',)

class DetInventarioSolicitudAdmin(admin.ModelAdmin):
    list_display = ('pk', 'detsolicitud', 'inventario', 'cantidad')
    list_filter = ('inventario',)
    search_fields = ('pk', 'inventario')
    ordering = ('pk',)

class JornadaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'fecha_solicitud', 'fecha_jornada', 'jefe_comunidad', 'proceso_actual', 'estado')
    list_filter = ('jefe_comunidad', 'proceso_actual', 'estado')
    search_fields = ('pk', 'jefe_comunidad')
    ordering = ('pk', 'fecha_solicitud', 'fecha_jornada')

class DetJornadaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'cant_solicitada', 'cant_aprobada')
    search_fields = ('pk',)
    ordering = ('pk',)

class DetInventarioJornadaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'detjornada', 'inventario', 'cantidad')
    list_filter = ('inventario',)
    search_fields = ('pk', 'inventario')
    ordering = ('pk',)

class IngresoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'fecha', 'descripcion', 'tipo_ingreso')
    list_filter = ('tipo_ingreso',)
    search_fields = ('pk', 'tipo_ingreso')
    ordering = ('pk', 'fecha')

class DetIngresoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ingreso', 'inventario', 'cantidad', 'lote')
    list_filter = ('inventario',)
    search_fields = ('pk',)
    ordering = ('pk',)

class TipoMoviAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nombre', 'operacion')
    search_fields = ('pk', 'nombre')
    ordering = ('pk', 'nombre')

class HistorialAdmin(admin.ModelAdmin):
    list_display = ('pk', 'fecha_mov', 'tipo_mov', 'empleado', 'producto', 'cantidad')
    list_filter = ('producto',)
    search_fields = ('pk', 'producto')
    ordering = ('pk', 'fecha_mov')

class ContabilidadFisicaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'fecha', 'proceso_actual', 'estado')
    list_filter = ('fecha', 'proceso_actual', 'estado')
    search_fields = ('pk', 'fecha')
    ordering = ('pk', 'fecha')
    # readonly_fields = ('date_of_birth',)

class DetContabilidadFisicaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'cantidad_contada', 'cantidad_inventario')
    search_fields = ('pk',)
    ordering = ('pk',)
    # readonly_fields = ('date_of_birth',)

class InventarioContFisicaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'detcontabilidad', 'inventario', 'cantidad_contada', 'cantidad_inventario')
    list_filter = ('inventario',)
    search_fields = ('pk', 'inventario')
    ordering = ('pk',)
    # readonly_fields = ('date_of_birth',)

class EgresoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'fecha', 'descripcion', 'tipo_egreso')
    list_filter = ('tipo_egreso',)
    search_fields = ('pk', 'tipo_egreso')
    ordering = ('pk', 'fecha')

class DetEgresoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'egreso', 'inventario', 'cantidad')
    list_filter = ('inventario',)
    search_fields = ('pk',)
    ordering = ('pk',)

admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(DetalleSolicitud, DetSolicitudAdmin)
admin.site.register(Jornada, JornadaAdmin)
admin.site.register(DetalleJornada, DetJornadaAdmin)
admin.site.register(Ingreso, IngresoAdmin)
admin.site.register(DetalleIngreso, DetIngresoAdmin)
admin.site.register(TipoMov, TipoMoviAdmin)
admin.site.register(Historial, HistorialAdmin)
admin.site.register(DetalleIventarioSolicitud, DetInventarioSolicitudAdmin)
admin.site.register(DetalleIventarioJornada, DetInventarioJornadaAdmin)
admin.site.register(ContabilidadFisica, ContabilidadFisicaAdmin)
admin.site.register(DetContabilidadFisica, DetContabilidadFisicaAdmin)
admin.site.register(InventarioContFisica, InventarioContFisicaAdmin)
admin.site.register(Egreso, EgresoAdmin)
admin.site.register(DetalleEgreso, DetEgresoAdmin)