from rest_framework import serializers
from .models import (
    Estado,
    LocalidadCaserio,
    Pais,
    UnidadMedida,
    ConversionUnidadMedida,
    Mercado,
    Departamento,
    Provincia,
    Distrito,
)


class UnidadMedidaSerializer(serializers.ModelSerializer):

    class Meta:

        model = UnidadMedida
        fields = "__all__"


class ConversionUnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:

        model = ConversionUnidadMedida
        fields = "__all__"


class MercadoSerializer(serializers.ModelSerializer):
    class Meta:

        model = Mercado
        fields = "__all__"


class PaisSerializer(serializers.ModelSerializer):

    class Meta:

        model = Pais
        fields = "__all__"

class DepartamentoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Departamento
        fields = "__all__"


class ProvinciaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Provincia
        fields = "__all__"


class DistritoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Distrito
        fields = "__all__"
        

class LocalidadCaserioSerializer(serializers.ModelSerializer):

    class Meta:

        model = LocalidadCaserio
        fields = "__all__"
