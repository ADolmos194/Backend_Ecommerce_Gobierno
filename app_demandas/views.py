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
def listar_tiposdemandas(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Tipos de demandas no encontradas",
        "message_user": "Tipos de demandas no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        tp.id,
                        tp.nombre
                    FROM TiposDemandas tp
                    WHERE tp.estado_id IN (1)
                    ORDER BY tp.id DESC 
                    """
                )
                dic_tiposdemandas = ConvertirQueryADiccionarioDato(cursor)
                cursor.close()

            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Tipos de demandas obtenidas correctamente",
                    "message": "Tipos de demandas obtenidas correctamente",
                    "data": dic_tiposdemandas,
                }
            )
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(f"Error al listar los tipos de demandas: {str(e)}")
            dic_response.update(
                {"message": "Error al listar los tipos de demandas", "data": str(e)}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@transaction.atomic
def listar_demandas(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Demandas no encontradas",
        "message_user": "Demandas no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        d.id,
                        d.tiposdemandas_id,
                        td.nombre AS nombre_tipodemanda,
                        d.url_imagen,
                        d.fecha_publicacion,
                        d.tipoproducto_id,
                        tipro.nombre AS nombre_tipoproducto,
                        d.producto_id,
                        pro.nombre AS nombre_producto,
                        d.descripcion,
                        d.nota,
                        d.localidadcaserio_id,
                        lc.nombre AS nombre_localidadcaserio,
                        d.referencia_ubicacion,
                        d.direccion,
                        d.contacto,
                        d.telefono,
                        d.email,
                        d.usuariosistema_id,
                        us.usuario AS nombre_usuario,
                        d.estado_id,
                        TO_CHAR(d.fecha_creacion AT TIME ZONE 'America/Lima', 'YYYY-MM-DD HH24:MI:SS') AS fecha_creacion,
                        TO_CHAR(d.fecha_modificacion AT TIME ZONE 'America/Lima', 'YYYY-MM-DD HH24:MI:SS') AS fecha_modificacion
                    FROM Demandas d
                    LEFT JOIN LocalidadCaserio lc ON d.localidadcaserio_id = lc.id
                    LEFT JOIN Distrito di ON lc.distrito_id = di.id
                    LEFT JOIN Provincia pr ON di.provincia_id = pr.id
                    LEFT JOIN Tiposdemandas td ON d.tiposdemandas_id = td.id
                    LEFT JOIN Producto pro ON d.producto_id = pro.id
                    LEFT JOIN TipoProducto tipro ON d.tipoproducto_id = tipro.id
                    LEFT JOIN UsuarioSistema us ON d.usuariosistema_id = us.id
                    WHERE d.estado_id IN (1, 2)
                    AND d.usuariosistema_id = %s
                    ORDER BY d.id DESC
                    """,
                    [id]
                )
                dic_demandas = ConvertirQueryADiccionarioDato(cursor)

            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Demandas obtenidas correctamente",
                    "message": "Demandas obtenidas correctamente",
                    "data": dic_demandas,
                }
            )
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(f"Error al listar la demandas: {str(e)}")
            dic_response.update(
                {
                    "message": "Error al listar la demandas",
                    "data": str(e),
                }
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)


@api_view(["POST"])
@transaction.atomic
def crear_demandas(request):

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

            serializer = DemandasSerializer(data=data)

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
def actualizar_demandas(request, id):

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
                queryset = Demandas.objects.using("default").get(
                    id=id
                )
            except Demandas.DoesNotExist:

                return JsonResponse(
                    dic_response, safe=False, status=status.HTTP_404_NOT_FOUND
                )

            serializer = DemandasSerializer(queryset, data=data)

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
def eliminar_demandas(request, id):

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
                queryset = Demandas.objects.using("default").get(
                    id=id
                )

                queryset.estado = Estado.objects.using("default").get(
                    id=data["estado"]
                )
                queryset.fecha_modificacion = datetime.now(ZoneInfo("America/Lima"))

                queryset.save()

                serializer = DemandasSerializer(queryset)

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

            except Demandas.DoesNotExist:
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

