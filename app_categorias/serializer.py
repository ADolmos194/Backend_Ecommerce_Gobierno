from rest_framework import serializers
from .models import (
    TipoProducto,
    Producto
    )


class TipoProductoSerializer(serializers.ModelSerializer):

    class Meta:

        model = TipoProducto
        fields = "__all__"
        
class ProductoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Producto
        fields = "__all__"