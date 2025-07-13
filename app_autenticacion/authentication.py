from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import AuthenticationFailed
from app_autenticacion.models import UsuarioSistema

class UsuarioSistemaJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token["user_id"]
        except KeyError:
            raise InvalidToken("Token sin user_id")

        try:
            return UsuarioSistema.objects.get(pk=user_id)
        except UsuarioSistema.DoesNotExist:
            raise AuthenticationFailed("UsuarioSistema no encontrado", code="user_not_found")
