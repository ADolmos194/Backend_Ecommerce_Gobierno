from rest_framework import serializers
from .models import (
    PreciosMercadoMayoristaMinorista,
    PrecioCiudades
    )

################################################## APP_REGISTROS ############################################################
class PreciosMercadoMayoristaMinoristaSerializer(serializers.ModelSerializer):
    
    """
    Serializer para el modelo PreciosMercadoMayoristaMinorista. Este serializer se utiliza para convertir 
    los objetos de tipo PreciosMercadoMayoristaMinorista en representaciones JSON y viceversa.
    Permite la validación y serialización de datos de PreciosMercadoMayoristaMinorista en las vistas de la API.

    Utiliza todos los campos del modelo PreciosMercadoMayoristaMinorista.
    """
    
    class Meta:
        # Define el modelo que se va a serializar
        model = PreciosMercadoMayoristaMinorista
        
        # Incluye todos los campos del modelo en la serialización
        fields = '__all__' 
        
        
class PrecioCiudadesSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = PrecioCiudades
        fields = '__all__' 
        
