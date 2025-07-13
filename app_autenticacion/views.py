import json
import logging
from django.http import JsonResponse

from django.shortcuts import get_object_or_404
from rest_framework import status
from datetime import datetime
from zoneinfo import ZoneInfo

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db import connection, transaction, DatabaseError

from app_autenticacion.utils import generar_tokens_para_usuario
from app_autenticacion.models import Permiso, Rol

from .serializer import *
from django.contrib.auth.hashers import check_password

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


logger = logging.getLogger(__name__)


def ConvertirQueryADiccionarioDato(cursor):
    columna = [desc[0] for desc in cursor.description]
    return [dict(zip(columna, fila)) for fila in cursor.fetchall()]


@api_view(["GET"])
@transaction.atomic
def listar_tipodocumento(request):
    dic_response = {
        "code": 200,
        "status": "success",
        "message": "Lista de tipos de documento obtenida exitosamente",
        "message_user": "Tipos de documento obtenidos correctamente",
        "data": [],
    }

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nombre FROM tipodocumento WHERE estado_id = 1")
            data = ConvertirQueryADiccionarioDato(cursor)
            dic_response["data"] = data

    except DatabaseError as e:
        logger.error("Error al listar tipos de documento: %s" % str(e))
        dic_response.update({
            "code": 500,
            "status": "error",
            "message": "Error al obtener los tipos de documento",
            "message_user": "Error al obtener los tipos de documento",
            "data": {"error": str(e)},
        })
        return JsonResponse(dic_response, status=500)

    return JsonResponse(dic_response, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
@transaction.atomic
def verificacion_usuariosistema(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Credenciales inválidas",
        "message_user": "Usuario o contraseña incorrectos",
        "data": [],
    }

    serializer = LoginSerializer(data=request.data)

    if not serializer.is_valid():
        dic_response["data"] = serializer.errors
        dic_response["message_user"] = "Datos de entrada inválidos"
        dic_response["message"] = "Error de validación"
        return JsonResponse(dic_response, status=400)

    usuario = serializer.validated_data["usuario"]
    password = serializer.validated_data["password"]

    try:
        usuario_obj = UsuarioSistema.objects.get(usuario=usuario, estado_id=1)

        if not check_password(password, usuario_obj.password):
            return Response({
                "code": 401,
                "status": "error",
                "message": "Contraseña incorrecta",
                "message_user": "Usuario o contraseña incorrectos",
            }, status=401)

        # generar tokens
        tokens = generar_tokens_para_usuario(usuario_obj)
        usuario_data = UserSerializer(usuario_obj).data

        # obtener el menú según su rol
        permisos_qs = Permiso.objects.filter(
            rolpermiso__rol=usuario_obj.rol,
            estado__id=1,
            rolpermiso__rol__estado__id=1
        ).distinct()

        # construir árbol por categorías
        menu_dict = {}
        for permiso in permisos_qs:
            categoria = permiso.categoria or "Otros"
            if categoria not in menu_dict:
                menu_dict[categoria] = []
            menu_dict[categoria].append({
                "label": permiso.nombre,
                "icon": permiso.icono,
                "routerLink": [permiso.ruta]
            })

        # formatear para PrimeNG MenuItem[]
        menu_items = []
        for categoria, items in menu_dict.items():
            menu_items.append({
                "label": categoria,
                "items": items
            })

        return Response({
            "code": 200,
            "status": "success",
            "message": "Inicio de sesión exitoso",
            "message_user": "Bienvenido al sistema",
            "data": {
                "access": tokens["access"],
                "refresh": tokens["refresh"],
                "userData": usuario_data,
                "menu": menu_items
            },
        }, status=200)

    except UsuarioSistema.DoesNotExist:
        return Response({
            "code": 404,
            "status": "error",
            "message": "Usuario no encontrado o inactivo",
            "message_user": "Usuario no encontrado o inactivo",
        }, status=404)

    except Exception as e:
        logger.error("Error inesperado en verificación: %s" % str(e))
        dic_response.update({
            "message_user": "Error inesperado",
            "message": "Excepción durante la autenticación",
            "data": {"error": str(e)},
        })
        return JsonResponse(dic_response, status=500)


@api_view(["POST"])
@transaction.atomic
def crear_usuariosistema(request):

    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al crear al Usuario del sistema",
        "message_user": "Error al crear al Usuario",
        "data": [],
    }

    if request.method == "POST":

        try:

            data = json.loads(request.body)
            data["password"] = make_password(data["password"])
            data["estado"] = 1
            data["rol"] = 2
            data["fecha_creacion"] = datetime.now(ZoneInfo("America/Lima"))
            data["fecha_modificacion"] = datetime.now(ZoneInfo("America/Lima"))

            # Verificación con ORM
            if UsuarioSistema.objects.filter(
                nombrecompleto=data["nombrecompleto"],
                email=data["email"],
                estado_id__in=[1, 2]
            ).exists():
                dic_response.update({
                    "message_user": "Ya existe un usuario o email existente",
                    "message": "Ya hay un dato existente.",
                })
                return JsonResponse(dic_response, status=400)

            serializer = UsuarioSistemaSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                dic_response.update({
                    "code": 201,
                    "status": "success",
                    "message": "Usuario del sistema creado exitosamente",
                    "message_user": "Usuario del sistema creado exitosamente",
                    "data": serializer.data,
                })
                return JsonResponse(dic_response, status=201)

            dic_response["data"] = serializer.errors
            return JsonResponse(dic_response, status=400)

        except Exception as e:
            logger.error("Error inesperado al crear el Usuario del sistema: %s" % str(e))
            dic_response.update({
                "message_user": "Error inesperado",
                "data": {"error": str(e)},
            })
            return JsonResponse(dic_response, status=500)

    return JsonResponse(dic_response, status=200)

