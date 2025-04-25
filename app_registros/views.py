import json
import logging
from django.http import JsonResponse

from rest_framework import status
from datetime import datetime

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


# ----------------- Precios Mercado Mayorista Minorista ----------------- #

@api_view(["GET"])
@transaction.atomic
def listar_PreciosMercadoMayoristaMinorista(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Precios del Mercado Ma.Mi no encontrados",
        "message_user": "Precios del Mercado Ma.Mi no encontrados",
        "data": [],
    }
    if request.method == "GET":
        try:

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        pmmm.id,
                        pmmm.producto_id,
                        p.nombre as nombre_producto,
                        pmmm.unidadmedida_id,
                        um.nombre as nombre_unidadmedida,
                        pmmm.valor_equivalente_kilogramo_litro,
                        pmmm.precio_minimo,
                        pmmm.precio_promedio,
                        pmmm.precio_maximo,
                        pmmm.estado_id,
                        TO_CHAR(pmmm.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(pmmm.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion
                    FROM PreciosMercadoMayoristaMinorista pmmm
                    LEFT JOIN Producto p ON p.id = pmmm.producto_id
                    LEFT JOIN UnidadMedida um ON um.id = pmmm.unidadmedida_id
                    WHERE pmmm.estado_id IN (1, 2)
                    ORDER BY pmmm.id DESC
                    """
                )
                dic_precios = ConvertirQueryADiccionarioDato(cursor)
                cursor.close()

            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Precios del Mercado Ma.Mi obtenidos correctamente",
                    "message": "Precios del Mercado Ma.Mi obtenidos correctamente",
                    "data": dic_precios,
                }
            )
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(f"Error al listar los Precios del Mercado Ma.Mi: {str(e)}")
            dic_response.update(
                {"message": "Error al listar los Precios del Mercado Ma.Mi", "data": str(e)}
            )
            return JsonResponse(dic_response, status=500)
    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)

@api_view(["POST"])
@transaction.atomic
def crear_PreciosMercadoMayoristaMinorista(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al crear el Precio Mercado Ma.Mi",
        "message_user": "Error al crear el Precio Mercado Ma.Mi",
        "data": [],
    }

    if request.method == "POST":
        try:

            data = json.loads(request.body)
            data["estado"] = 1
            data["fecha_creacion"] = datetime.now()
            data["fecha_modificacion"] = datetime.now()

            serializer = PreciosMercadoMayoristaMinoristaSerializer(data=data)

            if serializer.is_valid():

                with connection.cursor() as cursor:

                    unidadmedida_id = data["unidadmedida"]

                    cursor.execute(
                        "SELECT unidadmedida_id FROM PreciosMercadoMayoristaMinorista WHERE (unidadmedida_id='{0}') and estado_id IN (1, 2)".format(
                            unidadmedida_id
                        )
                    )

                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {
                                "message_user": "Ya existe un Precio Mercado Ma.Mi con el mismo producto y unidad de medida",
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
                        "message_user": "Precio Mercado Ma.Mi creado exitosamente",
                        "message": "Precio Mercado Ma.Mi creado exitosamente",
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

            logger.error(f"Error inesperado al crear el Precio Mercado Ma.Mi: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)

@api_view(["PUT"])
@transaction.atomic
def actualizar_PreciosMercadoMayoristaMinorista(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al actualizar el Precio Mercado Ma.Mi",
        "message_user": "Error al actualizar el Precio Mercado Ma.Mi",
        "data": [],
    }

    if request.method == "PUT":
        try:

            data = json.loads(request.body)

            data["fecha_modificacion"] = datetime.now()

            try:
                queryset = PreciosMercadoMayoristaMinorista.objects.using("default").get(id=id)
            except PreciosMercadoMayoristaMinorista.DoesNotExist:

                return JsonResponse(
                    dic_response, safe=False, status=status.HTTP_404_NOT_FOUND
                )

            serializer = PreciosMercadoMayoristaMinoristaSerializer(queryset, data=data)

            if serializer.is_valid():

                with connection.cursor() as cursor:

                    unidadmedida_id = data["unidadmedida"]
                    estado = data["estado"]

                    cursor.execute(
                        "SELECT unidadmedida_id FROM PreciosMercadoMayoristaMinorista WHERE (unidadmedida_id='{0}') and estado_id = {1} and id <> {2}".format(
                            unidadmedida_id, estado, id
                        )
                    )
                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {
                                "message_user": "Ya existe un Precio Mercado Ma.Mi con el mismo producto y unidad de medida",
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
                        "message_user": "Precio Mercado Ma.Mi actualizado exitosamente",
                        "message": "Precio Mercado Ma.Mi actualizado exitosamente",
                        "data": serializer.data,
                    }
                )

                return JsonResponse(dic_response, status=200)

            dic_response.update(
                {
                    "message_user": "Datos inválidos.",
                    "data": serializer.errors,
                }
            )
            return JsonResponse(dic_response, status=400)

        except Exception as e:

            logger.error(f"Error inesperado al actualizar el Precio Mercado Ma.Mi: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)
        
    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@transaction.atomic
def eliminar_PreciosMercadoMayoristaMinorista(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al eliminar el Precio Mercado Ma.Mi",
        "message_user": "Error al eliminar el Precio Mercado Ma.Mi",
        "data": [],
    }

    if request.method == "DELETE":
        try:

            data = {"estado": 3}

            try:
                queryset = PreciosMercadoMayoristaMinorista.objects.using("default").get(id=id)

                queryset.estado = Estado.objects.using("default").get(id=data["estado"])
                queryset.fecha_modificacion = datetime.now()

                queryset.save()

                serializer = PreciosMercadoMayoristaMinoristaSerializer(queryset)

                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Precio Mercado Ma.Mi eliminado lógicamente",
                        "message": "Precio Mercado Ma.Mi eliminado lógicamente",
                        "data": serializer.data,
                    }
                )

                return JsonResponse(dic_response, status=200)

            except PreciosMercadoMayoristaMinorista.DoesNotExist:
                return JsonResponse(
                    dic_response, safe=False, status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            logger.error(f"Error inesperado al eliminar el Precio Mercado Ma.Mi: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
        
    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)


# ------------------ Precios Ciudades ----------------- #
@api_view(["GET"])
@transaction.atomic
def listar_PrecioCiudades(request):

    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Precios de las Ciudades no encontrados",
        "message_user": "Precios de las Ciudades no encontrados",
        "data": [],
    }
    if request.method == "GET":
        try:

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        pc.id,
                        pc.codigo,
                        pc.serie,
                        pc.codigo || '-' || pc.serie AS codigo_serie,
                        pc.producto_id,
                        p.nombre as nombre_producto,
                        pc.conversionunidadmedida_id,
                        cum.nombre as nombre_conversionunidadmedida,
                        pc.valor_enero,
                        pc.valor_febrero,
                        pc.valor_marzo,
                        pc.valor_abril,
                        pc.valor_mayo,
                        pc.valor_junio,
                        pc.valor_julio,
                        pc.valor_agosto,
                        pc.valor_septiembre,
                        pc.valor_octubre,
                        pc.valor_noviembre,
                        pc.valor_diciembre,
                        pc.estado_id,
                        TO_CHAR(pc.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(pc.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion
                    FROM PrecioCiudades pc
                    LEFT JOIN Producto p ON p.id = pc.producto_id
                    LEFT JOIN ConversionUnidadMedida cum ON cum.id = pc.conversionunidadmedida_id
                    WHERE pc.estado_id IN (1, 2)
                    ORDER BY pc.id DESC
                    """
                )
                dic_precios_ciudades = ConvertirQueryADiccionarioDato(cursor)
                cursor.close()
            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Precios de las Ciudades obtenidos correctamente",
                    "message": "Precios de las Ciudades obtenidos correctamente",
                    "data": dic_precios_ciudades,
                }
            )
            return JsonResponse(dic_response, status=200)
        except DatabaseError as e:
            logger.error(f"Error al listar los Precios de las Ciudades: {str(e)}")
            dic_response.update(
                {"message": "Error al listar los Precios de las Ciudades", "data": str(e)}
            )
            return JsonResponse(dic_response, status=500)   
    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)

@api_view(["POST"])
@transaction.atomic
def crear_PrecioCiudades(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al crear el Precio de las Ciudades",
        "message_user": "Error al crear el Precio de las Ciudades",
        "data": [],
    }

    if request.method == "POST":
        try:

            data = json.loads(request.body)
            data["estado"] = 1
            data["fecha_creacion"] = datetime.now()
            data["fecha_modificacion"] = datetime.now()

            serializer = PrecioCiudadesSerializer(data=data)

            if serializer.is_valid():

                with connection.cursor() as cursor:

                    conversionunidadmedida_id = data["conversionunidadmedida"]

                    cursor.execute(
                        "SELECT conversionunidadmedida_id FROM PrecioCiudades WHERE (conversionunidadmedida_id='{0}') and estado_id IN (1, 2)".format(
                            conversionunidadmedida_id
                        )
                    )

                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {
                                "message_user": "Ya existe un Precio de las Ciudades con el mismo producto y unidad de medida",
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
                        "message_user": "Precio de las Ciudades creado exitosamente",
                        "message": "Precio de las Ciudades creado exitosamente",
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

            logger.error(f"Error inesperado al crear el Precio de las Ciudades: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)
    
@api_view(["PUT"])
@transaction.atomic
def actualizar_PrecioCiudades(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al actualizar el Precio de las Ciudades",
        "message_user": "Error al actualizar el Precio de las Ciudades",
        "data": [],
    }

    if request.method == "PUT":
        try:

            data = json.loads(request.body)

            data["fecha_modificacion"] = datetime.now()

            try:
                queryset = PrecioCiudades.objects.using("default").get(id=id)
            except PrecioCiudades.DoesNotExist:

                return JsonResponse(
                    dic_response, safe=False, status=status.HTTP_404_NOT_FOUND
                )

            serializer = PrecioCiudadesSerializer(queryset, data=data)

            if serializer.is_valid():

                with connection.cursor() as cursor:

                    conversionunidadmedida_id = data["conversionunidadmedida"]
                    estado = data["estado"]

                    cursor.execute(
                        "SELECT conversionunidadmedida_id FROM PrecioCiudades WHERE (conversionunidadmedida_id='{0}') and estado_id = {1} and id <> {2}".format(
                            conversionunidadmedida_id, estado, id
                        )
                    )
                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {
                                "message_user": "Ya existe un Precio de las Ciudades con el mismo producto y unidad de medida",
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
                        "message_user": "Precio de las Ciudades actualizado exitosamente",
                        "message": "Precio de las Ciudades actualizado exitosamente",
                        "data": serializer.data,
                    }
                )

                return JsonResponse(dic_response, status=200)

            dic_response.update(
                {
                    "message_user": "Datos inválidos.",
                    "data": serializer.errors,
                }
            )
            return JsonResponse(dic_response, status=400)

        except Exception as e:

            logger.error(f"Error inesperado al actualizar el Precio de las Ciudades: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)
        
    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@transaction.atomic
def eliminar_PrecioCiudades(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al eliminar el Precio de las Ciudades",
        "message_user": "Error al eliminar el Precio de las Ciudades",
        "data": [],
    }

    if request.method == "DELETE":
        try:

            data = {"estado": 3}

            try:
                queryset = PrecioCiudades.objects.using("default").get(id=id)

                queryset.estado = Estado.objects.using("default").get(id=data["estado"])
                queryset.fecha_modificacion = datetime.now()

                queryset.save()

                serializer = PrecioCiudadesSerializer(queryset)

                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Precio de las Ciudades eliminado lógicamente",
                        "message": "Precio de las Ciudades eliminado lógicamente",
                        "data": serializer.data,
                    }
                )

                return JsonResponse(dic_response, status=200)

            except PrecioCiudades.DoesNotExist:
                return JsonResponse(
                    dic_response, safe=False, status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            logger.error(f"Error inesperado al eliminar el Precio de las Ciudades: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
        
    return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)

