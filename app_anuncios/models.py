from django.db import models

from app.models import Estado, UnidadMedida
from app_categorias.models import TipoProducto, Producto, SubProducto


class TipoAnuncio (models.Model):

    nombre = models.CharField(max_length=50, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "tipoanuncio"
        
    def __str__(self):
        return '%s' % (self.nombre)
    

class AnuncioCompraVenta(models.Model):
    
    tipoanuncio = models.ForeignKey(TipoAnuncio, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=50, null=True, blank= True)
    asunto = models.CharField(max_length=100, null=True, blank= True)
    descripcion = models.TextField(null=True, blank=True)
    unidadmedida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)
    tipoproducto = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    subproducto = models.ForeignKey(SubProducto, on_delete=models.CASCADE)
    precio = models.FloatField(null=True, blank=True)
    costo = models.FloatField(null=True, blank=True)
    termino =  models.TextField(null=True, blank=True)
    contacto = models.CharField(max_length=100, null=True, blank= True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "anunciocompraventa"
        
    def __str__(self):
        return '%s - %s - %s' % (self.titulo, self.asunto, self.producto)
    
    
class AnuncioTrabajo(models.Model):
    titulo = models.CharField(max_length=50, null=True, blank= True)
    descripcion = models.TextField(null=True, blank=True)
    salario = models.FloatField(null=True, blank=True)
    periodoingreso = fecha_creacion = models.DateTimeField(null=True, blank=True)
    periodofinal = fecha_creacion = models.DateTimeField(null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "anunciotrabajo"
        
    def __str__(self):
        return '%s - %s - %s' % (self.titulo, self.descripcion, self.salario)
    


class AnuncioMaquinaria(models.Model):
    titulo = models.CharField(max_length=50, null=True, blank= True)
    asunto = models.CharField(max_length=100, null=True, blank= True)
    descripcion = models.TextField(null=True, blank=True)
    tipomaquinaria = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    maquinaria = models.ForeignKey(Producto, on_delete=models.CASCADE)
    submaquinaria = models.ForeignKey(SubProducto, on_delete=models.CASCADE)
    precioalquiler = models.FloatField(null=True, blank=True)
    termino =  models.TextField(null=True, blank=True)
    contacto = models.CharField(max_length=100, null=True, blank= True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "anunciomaquinaria"
        
    def __str__(self):
        return '%s - %s - %s' % (self.titulo, self.descripcion, self.tipomaquinaria)