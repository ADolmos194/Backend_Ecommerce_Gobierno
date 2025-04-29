from django.db import models

from app_categorias.models import Producto
from app.models import Distrito, Estado, Provincia

class DemandaProductosAgropecuarios(models.Model):
    
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE)
    fecha_publicacion = models.DateField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    nota = models.TextField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    contacto = models.TextField(null=True, blank=True)
    telefono = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "demandaproductosagropecuarios"
        
    def __str__(self):
        return '%s' % (self.descripcion)
    
    
class DemandaProductosAgropecuariosDetalle(models.Model):
    
    demandaproductosagropecuarios = models.ForeignKey(DemandaProductosAgropecuarios, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes/demandas_productosagropecuarios/', null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "demandaproductosagropecuariosdetalle"
    
    def __str__(self):
        return '%s' % (self.producto)