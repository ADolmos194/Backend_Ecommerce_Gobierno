from rest_framework_simplejwt.tokens import RefreshToken

def generar_tokens_para_usuario(usuario):
    refresh = RefreshToken.for_user(usuario)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }

