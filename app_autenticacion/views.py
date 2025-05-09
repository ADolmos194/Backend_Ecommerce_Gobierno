import json
import logging
from django.http import JsonResponse

from rest_framework import status
from datetime import datetime
from zoneinfo import ZoneInfo

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection, transaction, DatabaseError

from .serializer import *
from .models import *
from django.contrib.auth.hashers import check_password
logger = logging.getLogger(__name__)

def ConvertirQueryADiccionarioDato(cursor):
    columna = [desc[0] for desc in cursor.description]
    return [dict(zip(columna, fila)) for fila in cursor.fetchall()]


@api_view(["POST"])
@transaction.atomic
def verificacion_usuariosistema(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Credenciales inválidas",
        "message_user": "Usuario o contraseña incorrectos",
        "data": [],
    }

    if request.method == "POST":
        try:
            data = json.loads(request.body)

            usuario = data.get('usuario', '')
            password = data.get('password', '')

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, usuario, password 
                    FROM usuariosistema 
                    WHERE usuario = %s AND estado_id IN (1)
                    """,
                    [usuario]
                )
                dic_credenciales = ConvertirQueryADiccionarioDato(cursor)

                if dic_credenciales:
                    usuario_db = dic_credenciales[0]
                    if check_password(password, usuario_db["password"]):
                        dic_response.update({
                            "code": 200,
                            "status": "success",
                            "message": "Autenticación exitosa",
                            "message_user": "Bienvenido al sistema",
                            "data": {
                                "id": usuario_db["id"],
                                "usuario": usuario_db["usuario"],
                            },
                        })
                        return JsonResponse(dic_response, status=200)
                    else:
                        dic_response.update({
                            "message": "Contraseña incorrecta",
                            "message_user": "Usuario o contraseña incorrectos"
                        })
                        return JsonResponse(dic_response, status=401)

                dic_response.update({
                    "message": "Usuario no encontrado o inactivo",
                    "message_user": "Usuario no encontrado o inactivo",
                    "data": []
                })
                return JsonResponse(dic_response, status=404)

        except Exception as e:
            logger.error(f"Error al verificar usuario: {str(e)}")
            return JsonResponse(dic_response, status=500)

    return JsonResponse(dic_response, status=200)
        

@api_view(["GET"])
@transaction.atomic
def listar_usuariosistema(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Usuarios Activos no encontradas",
        "message_user": "Usuarios Activos no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        us.id,
                        us.usuario as nombre
                    FROM UsuarioSistema us
                    WHERE us.estado_id IN (1)
                    ORDER BY us.id DESC
                    """
                )
                dic_usuariosactivos = ConvertirQueryADiccionarioDato(cursor)
                cursor.close()

            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Usuarios Activos obtenidas correctamente",
                    "message": "Usuarios Activos obtenidas correctamente",
                    "data": dic_usuariosactivos,
                }
            )
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(
                f"Error al listar a los Usuarios Activos: {str(e)}"
            )
            dic_response.update(
                {
                    "message": "Error al listar a los Usuarios Activos",
                    "data": str(e),
                }
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)



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
            data['password'] = make_password(data['password'])
            data["estado"] = 1
            data["fecha_creacion"] = datetime.now(ZoneInfo("America/Lima"))
            data["fecha_modificacion"] = datetime.now(ZoneInfo("America/Lima"))

            serializer = UsuarioSistemaSerializer(data=data)

            if serializer.is_valid():

                with connection.cursor() as cursor:
                    nombre = data["nombre"]
                    email = data["email"]

                    cursor.execute(
                        "SELECT usuario, email FROM UsuarioSistema WHERE nombre=%s AND email=%s AND estado_id IN (1, 2)",
                        [nombre, email]
                    )

                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {
                                "message_user": "Ya existe un usuario o email existente ",
                                "message": "Ya hay un dato existente.",
                            }
                        )
                        return JsonResponse(dic_response, status=400)


                    cursor.close()

                serializer.save()

                dic_response.update(
                    {
                        "code": 201,
                        "status": "success",
                        "message_user": "Usuario del sistema creado exitosamente",
                        "message": "Usuario del sistema creado exitosamente",
                        "data": serializer.data,
                    }
                )

                return JsonResponse(dic_response, status=201)

            dic_response.update(
                {
                    "data": serializer.errors,
                }
            )
            return JsonResponse(dic_response, status=400)

        except Exception as e:

            logger.error(f"Error inesperado al crear el Usuario del sistema: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)
    