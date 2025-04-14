from django.db import models

from app.models import Estado

class TipoProducto(models.Model):

    nombre = models.CharField(max_length=100, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tipoproducto"
        
    def __str__(self):
        return '%s' % (self.nombre)

class Producto(models.Model):
    tipoproducto = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "producto"
        
    def __str__(self):
        return '%s' % (self.nombre)