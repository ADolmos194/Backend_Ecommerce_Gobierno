from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

"""
    El modelo Estado representa una entidad que almacena el nombre de un estado o condición.
    Este modelo se puede utilizar en sistemas donde se requiera clasificar o almacenar estados 
    de objetos o procesos, como estados de órdenes, productos, etc.
"""
# Modelo de Estado

class Estado(models.Model):

    # Campo para almacenar el nombre del estado
    nombre = models.CharField(max_length=25, null=True, blank=True)
    
    # Fecha de creación automática del registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # Fecha de última modificación automática del registro
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        # Define el nombre de la tabla en la base de datos
        db_table = "estado"
        
    def __str__(self):
        
        """
        Método que devuelve una representación en cadena del modelo.
        En este caso, devuelve el nombre del estado.
        """
        return '%s' % (self.nombre)


class UnidadMedida(models.Model):

    nombre = models.CharField(max_length=50, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "unidadmedida"
        
    def __str__(self):
        return '%s' % (self.nombre)

class ConversionUnidadMedida(models.Model):

    nombre = models.CharField(max_length=50, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "conversionunidadmedida"
        
    def __str__(self):
        return '%s' % (self.nombre)

class Mercado(models.Model):

    nombre = models.CharField(max_length=100, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mercado"
        
    def __str__(self):
        return '%s' % (self.nombre)
    

class Pais(models.Model):

    nombre = models.CharField(max_length=100, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pais"
        
    def __str__(self):
        return '%s' % (self.nombre)
    
class Departamento(models.Model):

    nombre = models.CharField(max_length=100, null=True, blank=True)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "departamento"
        
    def __str__(self):
        return '%s' % (self.nombre)
    
class Provincia(models.Model):

    nombre = models.CharField(max_length=100, null=True, blank=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "provincia"
        
    def __str__(self):
        return '%s' % (self.nombre)
    
class Distrito(models.Model):

    nombre = models.CharField(max_length=100, null=True, blank=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)  
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "distrito"
        
    def __str__(self):
        return '%s' % (self.nombre)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("El usuario debe tener un nombre de usuario.")
        if not password:
            raise ValueError("El usuario debe tener una contraseña.")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('estado', 1)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    estado = models.SmallIntegerField(default=1)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "custom_user"

    def __str__(self):
        return self.username


    