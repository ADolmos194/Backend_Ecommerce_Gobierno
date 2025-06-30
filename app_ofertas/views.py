from django.shortcuts import render

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
def listar_ofertas(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Ofertas no encontradas",
        "message_user": "Ofertas no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        d.id,
                        d.tiposofertas_id,
                        td.nombre AS nombre_tipoOferta,
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
                        d.web,
                        d.usuariosistema_id,
                        us.usuario AS nombre_usuario,
                        d.estado_id,
                        TO_CHAR(d.fecha_creacion AT TIME ZONE 'America/Lima', 'YYYY-MM-DD HH24:MI:SS') AS fecha_creacion,
                        TO_CHAR(d.fecha_modificacion AT TIME ZONE 'America/Lima', 'YYYY-MM-DD HH24:MI:SS') AS fecha_modificacion
                    FROM ofertas d
                    LEFT JOIN LocalidadCaserio lc ON d.localidadcaserio_id = lc.id
                    LEFT JOIN Distrito di ON lc.distrito_id = di.id
                    LEFT JOIN Provincia pr ON di.provincia_id = pr.id
                    LEFT JOIN Tiposofertas td ON d.tiposofertas_id = td.id
                    LEFT JOIN Producto pro ON d.producto_id = pro.id
                    LEFT JOIN TipoProducto tipro ON d.tipoproducto_id = tipro.id
                    LEFT JOIN UsuarioSistema us ON d.usuariosistema_id = us.id
                    WHERE d.estado_id IN (1, 2)
                    AND d.usuariosistema_id = %s
                    ORDER BY d.id DESC
                    """,
                    [id]
                )
                dic_ofertas = ConvertirQueryADiccionarioDato(cursor)

            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Ofertas obtenidas correctamente",
                    "message": "Ofertas obtenidas correctamente",
                    "data": dic_ofertas,
                }
            )
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(f"Error al listar la ofertas: {str(e)}")
            dic_response.update(
                {
                    "message": "Error al listar la ofertas",
                    "data": str(e),
                }
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)


@api_view(["POST"])
@transaction.atomic
def crear_ofertas(request):

    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al crear la Oferta de productos",
        "message_user": "Error al crear la Oferta de productos",
        "data": [],
    }

    if request.method == "POST":
        try:

            data = json.loads(request.body)
            data["estado"] = 1
            data["fecha_creacion"] = datetime.now(ZoneInfo("America/Lima"))
            data["fecha_modificacion"] = datetime.now(ZoneInfo("America/Lima"))

            serializer = OfertasSerializer(data=data)

            if serializer.is_valid():

                serializer.save()

                dic_response.update(
                    {
                        "code": 201,
                        "status": "success",
                        "message_user": "Oferta de productos creado exitosamente",
                        "message": "Oferta de productos creado exitosamente",
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
                f"Error inesperado al crear la Oferta de productos: {str(e)}"
            )
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)
        
    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)


@api_view(["PUT"])
@transaction.atomic
def actualizar_ofertas(request, id):

    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al actualizar la Oferta de productos",
        "message_user": "Error al actualizar la Oferta de productos",
        "data": [],
    }

    if request.method == "PUT":
        try:

            data = json.loads(request.body)

            data["fecha_modificacion"] = datetime.now(ZoneInfo("America/Lima"))

            try:
                queryset = Ofertas.objects.using("default").get(
                    id=id
                )
            except Ofertas.DoesNotExist:

                return JsonResponse(
                    dic_response, safe=False, status=status.HTTP_404_NOT_FOUND
                )

            serializer = OfertasSerializer(queryset, data=data)

            if serializer.is_valid():

                serializer.save()

                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Oferta de productos actualizado exitosamente",
                        "message": "Oferta de productos actualizado exitosamente",
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
                f"Error inesperado al actualizar la Oferta de productos: {str(e)}"
            )
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@transaction.atomic
def eliminar_ofertas(request, id):

    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al eliminar la Oferta de productos",
        "message_user": "Error al eliminar la Oferta de productos",
        "data": [],
    }

    if request.method == "DELETE":
        try:

            data = {"estado": 3}

            try:
                queryset = Ofertas.objects.using("default").get(
                    id=id
                )

                queryset.estado = Estado.objects.using("default").get(
                    id=data["estado"]
                )
                queryset.fecha_modificacion = datetime.now(ZoneInfo("America/Lima"))

                queryset.save()

                serializer = OfertasSerializer(queryset)

                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Oferta de productos eliminado lógicamente",
                        "message": "Oferta de productos eliminado lógicamente",
                        "data": serializer.data,
                    }
                )

                return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)

            except Ofertas.DoesNotExist:
                return JsonResponse(
                    dic_response, safe=False, status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            logger.error(
                f"Error inesperado al eliminar la Oferta de productos: {str(e)}"
            )
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)


