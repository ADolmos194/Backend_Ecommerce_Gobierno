from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import TipoAnuncio, AnuncioCompraVenta, AnuncioMaquinaria, AnuncioTrabajo

class TipoAnuncioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoAnuncio
        fields = '__all__'
        
class AnuncioCompraVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnuncioCompraVenta
        fields = '__all__'


class AnuncioMaquinariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnuncioMaquinaria
        fields = '__all__'
        
class AnuncioTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnuncioTrabajo
        fields = '__all__'
        