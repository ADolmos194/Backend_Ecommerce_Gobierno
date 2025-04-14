from django.db import models

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
    
class Departamento(models.Model):

    nombre = models.CharField(max_length=100, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "departamento"
        
    def __str__(self):
        return '%s' % (self.nombre)
    
class Provincia(models.Model):

    nombre = models.CharField(max_length=100, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "provincia"
        
    def __str__(self):
        return '%s' % (self.nombre)
    
class Distrito(models.Model):

    nombre = models.CharField(max_length=100, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "distrito"
        
    def __str__(self):
        return '%s' % (self.nombre)


    