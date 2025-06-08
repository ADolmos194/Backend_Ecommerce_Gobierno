from django.db import models

from app.models import Estado

# Create your models here.
class TipoMaquinaria (models.Model):

    nombre = models.CharField(max_length=50, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.RESTRICT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "tipomaquinaria"
        
    def __str__(self):
        return '%s' % (self.nombre)

class Maquinaria (models.Model):

    nombre = models.CharField(max_length=50, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.RESTRICT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "maquinaria"
        
    def __str__(self):
        return '%s' % (self.nombre)
    
class SubMaquinaria (models.Model):

    nombre = models.CharField(max_length=50, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.RESTRICT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "submaquinaria"
        
    def __str__(self):
        return '%s' % (self.nombre)