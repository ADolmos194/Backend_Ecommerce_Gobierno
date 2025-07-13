from django.db import models

from app.models import Distrito, Estado


class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    class Meta:
        db_table = "rol"

    def __str__(self):
        return self.nombre
    
class Permiso(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    ruta = models.CharField(max_length=100)  # ej: '/ofertas/frutas'
    icono = models.CharField(max_length=50, null=True, blank=True)  # ej: 'pi pi-fw pi-id-card'
    categoria = models.CharField(max_length=50, null=True, blank=True)  # ej: 'Ofertas'
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = "permiso"

    def __str__(self):
        return self.nombre

class RolPermiso(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = "rol_permiso"

class UsuarioSistema(models.Model):
    nombrecompleto = models.CharField(max_length=50, null=True, blank=True)
    usuario = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    tipodocumento = models.CharField(max_length=50, null=True, blank=True)
    numerodocumento = models.CharField(max_length=11, null=True, blank=True)
    numero_celular = models.CharField(max_length=15, null=True, blank=True)
    numero_telefono = models.CharField(max_length=15, null=True, blank=True)
    distrito = models.ForeignKey(Distrito, null=True, blank=True, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    terminos_condiciones = models.BooleanField(default=False)  
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, default=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    class Meta:
        db_table = "usuariosistema"
        
    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return f'{self.nombrecompleto} - {self.usuario}'
    
    

