from datetime import date
from django.db import models
from django.forms import model_to_dict
from django.db.models import Q
from django.utils.formats import date_format

# ubicacion del producto
class Almacen(models.Model):
	nombre = models.CharField(max_length=60, blank=False, null=False)

	class Meta:
		verbose_name = 'Ubicación'
		verbose_name_plural = 'Ubicaciones'

	def __str__(self):
		return f'{self.nombre}'
	
	def toJSON(self):
		item = model_to_dict(self)
		return item
	
# tipo de insumo
class TipoInsumo(models.Model):
	nombre = models.CharField(max_length=60, blank=False, null=False)

	class Meta:
		verbose_name = 'Tipo de insumo'
		verbose_name_plural = 'Tipo de insumos'

	def __str__(self):
		return self.nombre

	def toJSON(self):
		item = model_to_dict(self)
		return item
	
# laboratorio
class Laboratorio(models.Model):
	nombre = models.CharField(max_length=60, blank=False, null=False)

	class Meta:
		verbose_name = 'Laboratorio'
		verbose_name_plural = 'Laboratorios'

	def __str__(self):
		return self.nombre

	def toJSON(self):
		item = model_to_dict(self)
		return item
	
# productos
class Producto(models.Model):

	class Seleccion(models.TextChoices):
		SI = 'SI', 'SÍ'
		NO = 'NO', 'NO'

	nombre = models.CharField(max_length=50, blank=False, null=False)
	almacen = models.ForeignKey(Almacen, verbose_name='Ubicación', on_delete=models.PROTECT, blank=False, null=False)
	tipo_insumo = models.ForeignKey(TipoInsumo, verbose_name='Tipo de insumo', on_delete=models.PROTECT, blank=False, null=False)
	laboratorio = models.ForeignKey(Laboratorio, verbose_name='Laboratorio', on_delete=models.PROTECT, blank=False, null=False)
	if_expire_date = models.CharField(verbose_name='Si caduca', max_length = 2, choices = Seleccion.choices)
	stock_minimo = models.IntegerField(default=0, blank=False, null=False)
	total_stock = models.IntegerField(default=0, null = False, blank= False)
	comprometido = models.IntegerField(default=0, verbose_name='Comprometido')

	def filtrar_inventario_reporte(self):
		filtro = self.inventario.filter(Q(comprometido__gt=0) | Q(stock__gt=0), producto_id=self.pk)
		return filtro

	def contar_productos(self):
		self.total_stock = 0
		self.comprometido = 0
		for s in self.inventario.filter(stock__gt=0):
			self.total_stock += s.stock
		for c in self.inventario.filter(comprometido__gt=0):
			self.comprometido += c.comprometido
		self.save()

	class Meta:
		verbose_name = 'Producto'
		verbose_name_plural = 'Productos'
		ordering = ['nombre']

	def __str__(self):
		return f'{self.nombre}'

	def toJSON(self):
		item = model_to_dict(self)
		item['almacen'] = {'nombre': self.almacen.nombre, 'id': self.almacen.pk}
		item['laboratorio'] = {'nombre':self.laboratorio.nombre, 'id': self.laboratorio.pk}
		item['tipo_insumo'] = {'nombre': self.tipo_insumo.nombre, 'id': self.tipo_insumo.pk}
		return item

class Inventario(models.Model):
	lote = models.CharField(max_length=50,verbose_name='Codigo de lote')
	f_vencimiento = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Fecha de vencimiento')
	stock = models.IntegerField(default=0, verbose_name='Stock')
	comprometido = models.IntegerField(default=0, verbose_name='Comprometido')
	producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='inventario', verbose_name='Producto')

	class Meta:
		verbose_name = 'Inventario'
		verbose_name_plural = 'Inventarios'
		# permissions = [
		# 	("can_view_student", "Can view student"),
		# ]

	def __str__(self):
		return "{} - {}".format(self.producto.nombre, self.lote)

	def toJSON(self):
		item = model_to_dict(self)
		item['nombre'] = self.producto.nombre
		item['fecha_vencimiento'] = date_format(self.f_vencimiento, "d/m/Y")
		item['cantidad_contada'] = 0
		return item
