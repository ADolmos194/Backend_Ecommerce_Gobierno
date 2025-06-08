from rest_framework import serializers
from .models import (
    Demandas
)

class DemandasSerializer(serializers.ModelSerializer):

    class Meta:

        model = Demandas
        fields = "__all__"
        
        
    

