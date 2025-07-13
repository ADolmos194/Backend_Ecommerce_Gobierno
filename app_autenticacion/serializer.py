from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import UsuarioSistema



class LoginSerializer(serializers.Serializer):
    usuario = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
    
class UsuarioSistemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioSistema
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioSistema
        fields = ["id", "usuario", "nombrecompleto", "email", "rol"]
        
        
class MenuItemSerializer(serializers.Serializer):
    label = serializers.CharField()
    icon = serializers.CharField(allow_null=True, allow_blank=True)
    routerLink = serializers.ListField(child=serializers.CharField())