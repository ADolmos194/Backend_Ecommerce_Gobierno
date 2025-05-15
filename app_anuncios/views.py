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


@api_view(["GET"])
@transaction.Atomic
def listar_tipoanuncio(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al listar los Tipos de Anuncios",
        "message_user": "Error al listar los Tipos de Anuncios",
        "data": [],
    }
    if request.method == "GET":
        try:

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id,
                        nombre,
                        TO_CHAR(fecha_creacion AT TIME ZONE 'America/Lima', 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(fecha_modificacion AT TIME ZONE 'America/Lima', 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion
                    FROM TipoAnuncio
                    WHERE id IN (1, 2)
                    ORDER BY id DESC
                    """
                )
                dic_tipoanuncio = ConvertirQueryADiccionarioDato(cursor)
                cursor.close()

            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Tipos de Anucios obtenidas correctamente",
                    "message": "Tipos de Anucios obtenidas correctamente",
                    "data": dic_tipoanuncio,
                }
            )
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(f"Error al listar los Tipos de Anuncios: {str(e)}")
            dic_response.update(
                {"message": "Error al listar os Tipos de Anuncios", "data": str(e)}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)


@api_view(["POST"])
@transaction.atomic
def crear_tipoanuncio(request):

    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al crear el Tipo de Anuncio",
        "message_user": "Error al crear el Tipo de Anuncio",
        "data": [],
    }

    if request.method == "POST":
        try:

            data = json.loads(request.body)
            data["estado"] = 1
            data["fecha_creacion"] = datetime.now(ZoneInfo("America/Lima"))
            data["fecha_modificacion"] = datetime.now(ZoneInfo("America/Lima"))

            serializer = TipoAnuncioSerializer(data=data)

            if serializer.is_valid():

                with connection.cursor() as cursor:

                    nombre = data["nombre"]

                    cursor.execute(
                        "SELECT nombre FROM TipoAnuncio WHERE nombre = %s AND estado_id IN (1, 2)", [nombre]
                    )

                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {
                                "message_user": "Ya existe un Tipo de Anuncio con el mismo Nombre",
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
                        "message_user": "Tipo de Anuncio creado exitosamente",
                        "message": "Tipo de Anuncio creado exitosamente",
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

            logger.error(f"Error inesperado al crear el Tipo de Anuncio: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)


@api_view(["PUT"])
@transaction.atomic
def actualizar_tipoanuncio(request, id):

    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al actualizar el Tipo de Anuncio",
        "message_user": "Error al actualizar el Tipo de Anuncio",
        "data": [],
    }

    if request.method == "PUT":
        try:

            data = json.loads(request.body)

            data["fecha_modificacion"] = datetime.now(ZoneInfo("America/Lima"))

            try:
                queryset = TipoAnuncio.objects.using("default").get(id=id)
            except TipoAnuncio.DoesNotExist:

                return JsonResponse(
                    dic_response, safe=False, status=status.HTTP_404_NOT_FOUND
                )

            serializer = TipoAnuncioSerializer(queryset, data=data)

            if serializer.is_valid():

                with connection.cursor() as cursor:

                    nombre = data["nombre"]
                    estado = data["estado"]

                    cursor.execute(
                        "SELECT nombre FROM TipoAnuncio WHERE nombre= %s AND estado_id = %s and id <> %s",[nombre, estado, id]
                    )
                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {
                                "message_user": "Ya existe un tipo de anuncio con el mismo nombre",
                                "message": "Ya hay un dato existente.",
                            }
                        )
                        return JsonResponse(dic_response, status=400)

                    cursor.close()

                serializer.save()

                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Tipo de Anuncio actualizado exitosamente",
                        "message": "Tipo de Anuncio actualizado exitosamente",
                        "data": serializer.data,
                    }
                )

                return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)

            dic_response.update(
                {
                    "message_user": "Datos inválidos.",
                    "data": serializer.errors,
                }
            )
            return JsonResponse(dic_response, status=400)

        except Exception as e:

            logger.error(
                f"Error inesperado al actualizar el Tipo de Anuncio: {str(e)}"
            )
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@transaction.atomic
def eliminar_tipoanuncio(request, id):

    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al eliminar el Tipo de Anuncio",
        "message_user": "Error al eliminar el Tipo de Anuncio",
        "data": [],
    }

    if request.method == "DELETE":
        try:

            data = {"estado": 3}

            try:
                queryset = TipoAnuncio.objects.using("default").get(id=id)

                queryset.estado = Estado.objects.using("default").get(id=data["estado"])
                queryset.fecha_modificacion = datetime.now(ZoneInfo("America/Lima"))

                queryset.save()

                serializer = TipoAnuncioSerializer(queryset)

                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Tipo de Anuncio eliminado lógicamente",
                        "message": "Tipo de Anuncion eliminado lógicamente",
                        "data": serializer.data,
                    }
                )

                return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)

            except TipoAnuncio.DoesNotExist:
                return JsonResponse(
                    dic_response, safe=False, status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            logger.error(f"Error inesperado al eliminar el Tipo de Anuncio: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)


