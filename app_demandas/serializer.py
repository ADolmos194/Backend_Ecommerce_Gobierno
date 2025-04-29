from rest_framework import serializers
from .models import (
    DemandaProductosAgropecuarios
)

class DemandaProductosAgropecuariosSerializer(serializers.ModelSerializer):

    class Meta:

        model = DemandaProductosAgropecuarios
        fields = "__all__"
