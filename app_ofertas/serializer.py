from rest_framework import serializers
from .models import (
    Ofertas
)

class OfertasSerializer(serializers.ModelSerializer):

    class Meta:

        model = Ofertas
        fields = "__all__"
        
        
    

