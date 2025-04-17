from django.db import models

from app_categorias.models import Producto
from app.models import Distrito, Estado, Provincia

class OfertasServicioAgrario(models.Model):
    
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes/ofertas_servicioagrario/', null=True, blank=True)
    fecha_publicacion = models.DateField(null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    descripcion = models.TextField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    contacto = models.TextField(null=True, blank=True)
    telefono = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    web = models.CharField(max_length=255, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ofertasservicioagrario"
        
    def __str__(self):
        return '%s' % (self.descripcion)
    

class OfertasProductosLacteos(models.Model):
    
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes/ofertas_productoslacteos/', null=True, blank=True)
    fecha_publicacion = models.DateField(null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    descripcion = models.TextField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    contacto = models.TextField(null=True, blank=True)
    telefono = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    web = models.CharField(max_length=255, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ofertasproductoslacteos"
        
    def __str__(self):
        return '%s' % (self.descripcion)
    
class OfertasFrutas(models.Model):
    
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes/ofectas_frutas/', null=True, blank=True)
    fecha_publicacion = models.DateField(null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    descripcion = models.TextField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    contacto = models.TextField(null=True, blank=True)
    telefono = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    web = models.CharField(max_length=255, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ofectasfrutas"
        
    def __str__(self):
        return '%s' % (self.descripcion)

class OfertasInsumoTecnologico(models.Model):
    
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes/ofertas_insumotecnologico/', null=True, blank=True)
    fecha_publicacion = models.DateField(null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    descripcion = models.TextField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    contacto = models.TextField(null=True, blank=True)
    telefono = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    web = models.CharField(max_length=255, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ofertasinsumotecnologico"
        
    def __str__(self):
        return '%s' % (self.descripcion)
    
class OfertasCerealesLegumbres(models.Model):
    
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes/ofertas_cerealeslegumbres/', null=True, blank=True)
    fecha_publicacion = models.DateField(null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    descripcion = models.TextField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    contacto = models.TextField(null=True, blank=True)
    telefono = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    web = models.CharField(max_length=255, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ofertascerealeslegumbres"
        
    def __str__(self):
        return '%s' % (self.descripcion)
    
class OfertasTuberculosRaices(models.Model):
    
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes/ofertas_tuberculosraices/', null=True, blank=True)
    fecha_publicacion = models.DateField(null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    descripcion = models.TextField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    contacto = models.TextField(null=True, blank=True)
    telefono = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    web = models.CharField(max_length=255, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ofertastuberculosraices"
        
    def __str__(self):
        return '%s' % (self.descripcion)
    
class OfertasPastosForrajes(models.Model):
    
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes/ofertas_pastosforrajes/', null=True, blank=True)
    fecha_publicacion = models.DateField(null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    descripcion = models.TextField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    contacto = models.TextField(null=True, blank=True)
    telefono = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    web = models.CharField(max_length=255, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ofertaspastosforrajes"
        
    def __str__(self):
        return '%s' % (self.descripcion)