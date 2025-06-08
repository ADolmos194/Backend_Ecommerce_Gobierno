from django.db import models

from app_categorias.models import Producto
from app.models import Estado, UnidadMedida, ConversionUnidadMedida, Mercado, Departamento, Provincia

class PreciosMercadoMayoristaMinorista(models.Model):

    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    unidadmedida = models.ForeignKey(UnidadMedida, on_delete=models.RESTRICT)
    valor_equivalente_kilogramo_litro = models.FloatField(null=True, blank=True)
    precio_minimo = models.FloatField(null=True, blank=True)
    precio_promedio = models.FloatField(null=True, blank=True)
    precio_maximo = models.FloatField(null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.RESTRICT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "preciosmercadomayoristaminorista"
        
    def __str__(self):
        return '%s - %s - %s' % (self.producto, self.unidadmedida, self.precio_minimo)
    
class PrecioCiudades(models.Model):
    codigo = models.CharField(max_length=50, null=True, blank=True)
    serie = models.CharField(max_length=100, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    conversionunidadmedida = models.ForeignKey(ConversionUnidadMedida, on_delete=models.RESTRICT)
    valor_anual = models.FloatField(null=True, blank=True)
    valor_enero = models.FloatField(null=True, blank=True)
    valor_febrero = models.FloatField(null=True, blank=True)
    valor_marzo = models.FloatField(null=True, blank=True)
    valor_abril = models.FloatField(null=True, blank=True)
    valor_mayo = models.FloatField(null=True, blank=True)
    valor_junio = models.FloatField(null=True, blank=True)
    valor_julio = models.FloatField(null=True, blank=True)
    valor_agosto = models.FloatField(null=True, blank=True)
    valor_septiembre = models.FloatField(null=True, blank=True)
    valor_octubre = models.FloatField(null=True, blank=True)
    valor_noviembre = models.FloatField(null=True, blank=True)
    valor_diciembre = models.FloatField(null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.RESTRICT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "preciociudades"
        
    def __str__(self):
        return '%s - %s - %s' % (self.producto, self.unidadmedida, self.precio_minimo)