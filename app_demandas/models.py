from django.db import models

from app_categorias.models import Producto, TipoProducto
from app.models import Distrito, Estado, Provincia
from app_autenticacion.models import UsuarioSistema

class DemandaProductosAgropecuarios(models.Model):
    
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE)
    fecha_publicacion = models.DateField(null=True, blank=True)
    tipoproducto = models.ForeignKey(TipoProducto, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    url_imagen = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    nota = models.TextField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    contacto = models.TextField(null=True, blank=True)
    telefono = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    usuariosistema = models.ForeignKey(UsuarioSistema, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "demandaproductosagropecuarios"
        
    def __str__(self):
        return '%s' % (self.descripcion)
    
    