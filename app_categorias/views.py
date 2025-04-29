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


# -> CRUD de Tipo Producto
api_view(['GET'])
@transaction.atomic
def listar_tipoproducto(request):
    
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Tipo de producto no encontradas",
        "message_user": "Tipo de producto no encontradas",
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
                        estado_id,
                        TO_CHAR(fecha_creacion AT TIME ZONE 'America/Lima', 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(fecha_modificacion AT TIME ZONE 'America/Lima', 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion
                    FROM TipoProducto
                    WHERE estado_id IN (1, 2)
                    ORDER BY id DESC
                    """
                )
                dic_tipoproducto = ConvertirQueryADiccionarioDato(cursor)
                cursor.close()

            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Tipo de producto obtenidas correctamente",
                    "message": "Tipo de producto obtenidas correctamente",
                    "data": dic_tipoproducto,
                }
            )
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(f"Error al listar el tipo de producto: {str(e)}")
            dic_response.update(
                {"message": "Error al listar el tipo de producto", "data": str(e)}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
@transaction.atomic
def listar_tipoproducto_activo(request):
    
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Tipo de productos activos no encontradas",
        "message_user": "Tipo de productos activos no encontradas",
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
                        estado_id,
                        TO_CHAR(fecha_creacion AT TIME ZONE 'America/Lima', 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(fecha_modificacion AT TIME ZONE 'America/Lima', 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion
                    FROM TipoProducto
                    WHERE estado_id IN (1)
                    ORDER BY id DESC
                    """
                )
                dic_tipoproducto_activo = ConvertirQueryADiccionarioDato(cursor)
                cursor.close()

            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Tipo de productos acitovos obtenidos correctamente",
                    "message": "Tipo de productos activos obtenidos correctamente",
                    "data": dic_tipoproducto_activo,
                }
            )
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(f"Error al listar el tipo de productos activos: {str(e)}")
            dic_response.update(
                {"message": "Error al listar el tipo de productos activos", "data": str(e)}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_200_OK)


@api_view(['POST'])
@transaction.atomic
def crear_tipoproducto(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al crear el tipo de producto",
        "message_user": "Error al crear el tipo de producto",
        "data": [],
    }
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            data["estado"] = 1 
            data["fecha_creacion"] = datetime.now(ZoneInfo("America/Lima"))
            data["fecha_modificacion"] = datetime.now(ZoneInfo("America/Lima"))

            serializer = TipoProductoSerializer(data=data)

            if serializer.is_valid():
            
                with connection.cursor() as cursor:

                    nombre = data["nombre"]
                    
                    cursor.execute(
                        "SELECT nombre FROM TipoProducto WHERE (nombre='{0}') and estado_id IN (1, 2)".format(nombre)
                    )

                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {"message_user": "Ya existe un tipo de producto con el mismo nombre", "message": "Ya hay un dato existente."}
                        )
                        return JsonResponse(dic_response, status=400)
                cursor.close()
                serializer.save()
                dic_response.update(
                    {
                        "code": 201,
                        "status": "success",
                        "message_user": "Tipo de producto creado exitosamente",
                        "message": "Tipo de producto creado exitosamente",
                        "data": serializer.data
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
            logger.error(f"Error inesperado al crear el tipo de producto: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)
    
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(['PUT'])
@transaction.atomic
def actualizar_tipoproducto(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al actualizar el tipo de producto",
        "message_user": "Error al actualizar el tipo de producto",
        "data": [],
    }

    if request.method == "PUT":
        try:
            
            data = json.loads(request.body)
            
            data["fecha_modificacion"] = datetime.now(ZoneInfo("America/Lima"))

            try:
                queryset = TipoProducto.objects.using('default').get(id=id)
            except TipoProducto.DoesNotExist:
                
                return JsonResponse(dic_response, safe=False, status=status.HTTP_404_NOT_FOUND)

            serializer = TipoProductoSerializer(queryset, data=data)

            if serializer.is_valid():

                with connection.cursor() as cursor:

                    nombre = data["nombre"]
                    estado = data["estado"]
                    
                    cursor.execute("SELECT nombre FROM TipoProducto WHERE (nombre='{0}') and estado_id = {1} and id <> {2}".format(nombre, estado, id))
                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {"message_user": "Ya existe un tipo de producto con el mismo nombre", "message": "Ya hay un dato existente."}
                        )
                        return JsonResponse(dic_response, status=400)

                    cursor.close()
                serializer.save()
                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Tipo de producto actualizado exitosamente",
                        "message": "Tipo de producto actualizado exitosamente",
                        "data": serializer.data
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
            logger.error(f"Error inesperado al actualizar el tipo de producto: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)
        
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@transaction.atomic
def eliminar_tipoproducto(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al eliminar el tipo de producto",
        "message_user": "Error al eliminar el tipo de producto",
        "data": [],
    }

    if request.method == "DELETE":
        try:

            data = {"estado": 3}        

            try:
                queryset = TipoProducto.objects.using('default').get(id=id)

                queryset.estado = Estado.objects.using('default').get(id=data["estado"])
                queryset.fecha_modificacion = datetime.now(ZoneInfo("America/Lima"))
                
                queryset.save()

                serializer = TipoProductoSerializer(queryset)

                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Tipo de producto eliminado lógicamente",
                        "message": "Tipo de producto eliminado lógicamente",
                        "data": serializer.data,
                    }
                )

                return JsonResponse(dic_response, status=200)

            except TipoProducto.DoesNotExist:
                return JsonResponse(dic_response, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error inesperado al eliminar el tipo de producto: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)


# -> CRUD de Producto

@api_view(['GET'])
@transaction.atomic
def listar_producto(request):
    
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Producto no encontradas",
        "message_user": "Producto no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        p.id,
                        p.nombre,
                        p.tipoproducto_id,
                        tp.nombre as nombre_tipoproducto,
                        p.codigo,
                        p.serie,
                        p.estado_id,
                        TO_CHAR(p.fecha_creacion AT TIME ZONE 'America/Lima', 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(p.fecha_modificacion AT TIME ZONE 'America/Lima', 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion
                    FROM Producto p
                    LEFT JOIN TipoProducto tp ON p.tipoproducto_id = tp.id
                    WHERE p.estado_id IN (1, 2)
                    ORDER BY p.id DESC
                    """
                )
                dic_producto = ConvertirQueryADiccionarioDato(cursor)
                cursor.close()

            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Producto obtenidas correctamente",
                    "message": "Producto obtenidas correctamente",
                    "data": dic_producto,
                }
            )
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(f"Error al listar el producto: {str(e)}")
            dic_response.update(
                {"message": "Error al listar el producto", "data": str(e)}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_200_OK)


@api_view(['GET'])
@transaction.atomic
def listar_producto_activo(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Producto activos no encontradas",
        "message_user": "Producto activos no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        p.id,
                        p.nombre,
                        p.codigo,
                        p.serie,
                        p.estado_id,
                        TO_CHAR(p.fecha_creacion AT TIME ZONE 'America/Lima', 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(p.fecha_modificacion AT TIME ZONE 'America/Lima', 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion
                    FROM Producto p
                    LEFT JOIN TipoProducto tp ON p.tipoproducto_id = tp.id
                    WHERE p.estado_id IN (1)
                    ORDER BY p.id DESC
                    """
                )
                dic_producto_activo = ConvertirQueryADiccionarioDato(cursor)
                cursor.close()

            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Producto acitovos obtenidos correctamente",
                    "message": "Producto activos obtenidos correctamente",
                    "data": dic_producto_activo,
                }
            )
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(f"Error al listar el producto activos: {str(e)}")
            dic_response.update(
                {"message": "Error al listar el producto activos", "data": str(e)}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_200_OK)


@api_view(['POST'])
@transaction.atomic
def crear_producto(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al crear el producto",
        "message_user": "Error al crear el producto",
        "data": [],
    }
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            data["estado"] = 1 
            data["fecha_creacion"] = datetime.now(ZoneInfo("America/Lima"))
            data["fecha_modificacion"] = datetime.now(ZoneInfo("America/Lima"))

            serializer = ProductoSerializer(data=data)

            if serializer.is_valid():
            
                with connection.cursor() as cursor:

                    nombre = data["nombre"]
                    
                    cursor.execute(
                        "SELECT nombre FROM Producto WHERE (nombre='{0}') and estado_id IN (1, 2)".format(nombre)
                    )

                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {"message_user": "Ya existe un producto con el mismo nombre", "message": "Ya hay un dato existente."}
                        )
                        return JsonResponse(dic_response, status=400)
                cursor.close()
                serializer.save()
                dic_response.update(
                    {
                        "code": 201,
                        "status": "success",
                        "message_user": "Producto creado exitosamente",
                        "message": "Producto creado exitosamente",
                        "data": serializer.data
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
            logger.error(f"Error inesperado al crear el producto: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)
    
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(['PUT'])
@transaction.atomic
def actualizar_producto(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al actualizar el producto",
        "message_user": "Error al actualizar el producto",
        "data": [],
    }

    if request.method == "PUT":
        try:
            
            data = json.loads(request.body)
            
            data["fecha_modificacion"] = datetime.now(ZoneInfo("America/Lima"))

            try:
                queryset = Producto.objects.using('default').get(id=id)
            except Producto.DoesNotExist:
                
                return JsonResponse(dic_response, safe=False, status=status.HTTP_404_NOT_FOUND)

            serializer = ProductoSerializer(queryset, data=data)

            if serializer.is_valid():

                with connection.cursor() as cursor:

                    nombre = data["nombre"]
                    estado = data["estado"]
                    
                    cursor.execute("SELECT nombre FROM Producto WHERE (nombre='{0}') and estado_id = {1} and id <> {2}".format(nombre, estado, id))
                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {"message_user": "Ya existe un producto con el mismo nombre", "message": "Ya hay un dato existente."}
                        )
                        return JsonResponse(dic_response, status=400)

                    cursor.close()
                serializer.save()
                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Producto actualizado exitosamente",
                        "message": "Producto actualizado exitosamente",
                        "data": serializer.data
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
            logger.error(f"Error inesperado al actualizar el producto: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)
        
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@transaction.atomic
def eliminar_producto(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al eliminar el producto",
        "message_user": "Error al eliminar el producto",
        "data": [],
    }

    if request.method == "DELETE":
        try:

            data = {"estado": 3}        

            try:
                queryset = Producto.objects.using('default').get(id=id)

                queryset.estado = Estado.objects.using('default').get(id=data["estado"])
                queryset.fecha_modificacion = datetime.now(ZoneInfo("America/Lima"))
                
                queryset.save()

                serializer = ProductoSerializer(queryset)

                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Producto eliminado lógicamente",
                        "message": "Producto eliminado lógicamente",
                        "data": serializer.data,
                    }
                )

                return JsonResponse(dic_response, status=200)

            except Producto.DoesNotExist:
                return JsonResponse(dic_response, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error inesperado al eliminar el producto: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)
