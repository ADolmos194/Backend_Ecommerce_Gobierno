from django.db import models

from app.models import Distrito, Estado, Provincia

class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=50, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.RESTRICT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tipodocumento"

    def __str__(self):
        return '%s' % (self.nombre)


class UsuarioSistema(models.Model):
    nombrecompleto = models.CharField(max_length=50, null=True, blank=True)
    usuario = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    tipodedocumento = models.ForeignKey(TipoDocumento, on_delete=models.RESTRICT)
    numerodedocumento = models.CharField(max_length=11, null=True, blank=True)
    numero_celular = models.CharField(max_length=15, null=True, blank=True)
    numero_telefono = models.CharField(max_length=15, null=True, blank=True)
    provincia = models.ForeignKey(Provincia, null=True, blank=True, on_delete=models.RESTRICT)
    distrito = models.ForeignKey(Distrito, null=True, blank=True, on_delete=models.RESTRICT)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    terminos_condiciones = models.BooleanField(default=False)  
    estado = models.ForeignKey(Estado, on_delete=models.RESTRICT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "usuariosistema"

    def __str__(self):
        return f'{self.nombrerecompleto} ({self.usuario})'