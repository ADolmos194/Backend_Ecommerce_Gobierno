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

logger = logging.getLogger(__name__)


def ConvertirQueryADiccionarioDato(cursor):
    """
    Convierte el resultado de una consulta SQL (cursor) en una lista de diccionarios,
    donde las claves son los nombres de las columnas y los valores son los datos obtenidos.

    :param cursor: cursor de la consulta ejecutada
    :return: Lista de diccionarios con los resultados de la consulta
    """
    columna = [desc[0] for desc in cursor.description]
    return [dict(zip(columna, fila)) for fila in cursor.fetchall()]



@api_view(["GET"])
@transaction.atomic
def listar_demandaproductosagropecuarios(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Demanda de productos agropecuarios no encontradas",
        "message_user": "Demanda de productos agropecuarios no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        d.id,
                        d.provincia_id,
                        pr.nombre as nombre_provincia,
                        d.distrito_id,
                        di.nombre as nombre_distrito,
                        pr.nombre || '-' || di.nombre AS nombre_provincia_distrito,
                        d.fecha_publicacion,
                        d.tipoproducto_id,
                        tipro.nombre as nombre_tipoproducto,
                        d.producto_id,
                        pro.nombre as nombre_producto,
                        d.url_imagen,
                        d.descripcion,
                        d.nota,
                        d.direccion,
                        d.contacto,
                        d.telefono,
                        d.email,
                        d.estado_id,
                        TO_CHAR(d.fecha_creacion AT TIME ZONE 'America/Lima', 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(d.fecha_modificacion AT TIME ZONE 'America/Lima', 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion
                    FROM DemandaProductosAgropecuarios d
                    LEFT JOIN Provincia pr ON d.provincia_id = pr.id
                    LEFT JOIN Distrito di ON d.distrito_id = di.id
                    LEFT JOIN Producto pro ON d.producto_id = pro.id
                    LEFT JOIN TipoProducto tipro ON d.tipoproducto_id = tipro.id
                    WHERE d.estado_id IN (1, 2)
                    ORDER BY d.id DESC
                    """
                )
                dic_demandaproductosagropecuarios = ConvertirQueryADiccionarioDato(cursor)
                cursor.close()

            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Demanda de productos agropecuarios obtenidas correctamente",
                    "message": "Demanda de productos agropecuarios obtenidas correctamente",
                    "data": dic_demandaproductosagropecuarios,
                }
            )
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(
                f"Error al listar la demanda de productos agropecuarios: {str(e)}"
            )
            dic_response.update(
                {
                    "message": "Error al listar la demanda de productos agropecuarios",
                    "data": str(e),
                }
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)


@api_view(["POST"])
@transaction.atomic
def crear_demandaproductosagropecuarios(request):

    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al crear la demanda de productos agropecuarios",
        "message_user": "Error al crear la demanda de productos agropecuarios",
        "data": [],
    }

    if request.method == "POST":
        try:

            data = json.loads(request.body)
            data["estado"] = 1
            data["fecha_creacion"] = datetime.now(ZoneInfo("America/Lima"))
            data["fecha_modificacion"] = datetime.now(ZoneInfo("America/Lima"))

            serializer = DemandaProductosAgropecuariosSerializer(data=data)

            if serializer.is_valid():

                serializer.save()

                dic_response.update(
                    {
                        "code": 201,
                        "status": "success",
                        "message_user": "Demanda de productos agropecuarios creado exitosamente",
                        "message": "Demanda de productos agropecuarios creado exitosamente",
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

            logger.error(
                f"Error inesperado al crear la demanda de productos agropecuarios: {str(e)}"
            )
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)
        
    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)


@api_view(["PUT"])
@transaction.atomic
def actualizar_demandaproductosagropecuarios(request, id):

    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al actualizar la demanda de productos agropecuarios",
        "message_user": "Error al actualizar la demanda de productos agropecuarios",
        "data": [],
    }

    if request.method == "PUT":
        try:

            data = json.loads(request.body)

            data["fecha_modificacion"] = datetime.now(ZoneInfo("America/Lima"))

            try:
                queryset = DemandaProductosAgropecuarios.objects.using("default").get(
                    id=id
                )
            except DemandaProductosAgropecuarios.DoesNotExist:

                return JsonResponse(
                    dic_response, safe=False, status=status.HTTP_404_NOT_FOUND
                )

            serializer = DemandaProductosAgropecuariosSerializer(queryset, data=data)

            if serializer.is_valid():

                serializer.save()

                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Demanda de productos agropecuarios actualizado exitosamente",
                        "message": "Demanda de productos agropecuarios actualizado exitosamente",
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
                f"Error inesperado al actualizar la demanda de productos agropecuarios: {str(e)}"
            )
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@transaction.atomic
def eliminar_demandaproductosagropecuarios(request, id):

    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al eliminar la demanda de productos agropecuarios",
        "message_user": "Error al eliminar la demanda de productos agropecuarios",
        "data": [],
    }

    if request.method == "DELETE":
        try:

            data = {"estado": 3}

            try:
                queryset = DemandaProductosAgropecuarios.objects.using("default").get(
                    id=id
                )

                queryset.estado = Estado.objects.using("default").get(
                    id=data["estado"]
                )
                queryset.fecha_modificacion = datetime.now(ZoneInfo("America/Lima"))

                queryset.save()

                serializer = DemandaProductosAgropecuariosSerializer(queryset)

                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Demanda de productos agropecuarios eliminado lógicamente",
                        "message": "Demanda de productos agropecuarios eliminado lógicamente",
                        "data": serializer.data,
                    }
                )

                return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)

            except DemandaProductosAgropecuarios.DoesNotExist:
                return JsonResponse(
                    dic_response, safe=False, status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            logger.error(
                f"Error inesperado al eliminar la demanda de productos agropecuarios: {str(e)}"
            )
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)

