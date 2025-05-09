from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import UsuarioSistema

class UsuarioSistemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioSistema
        fields = '__all__'