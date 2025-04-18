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


@api_view(["GET"])
@transaction.atomic
def listar_estado(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Estado no encontradas",
        "message_user": "Estado no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id,
                        nombre
                    FROM Estado
                    WHERE id IN (1, 2)
                    ORDER BY id DESC
                    """
                )
                dic_estado = ConvertirQueryADiccionarioDato(cursor)
                cursor.close()

            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Estados obtenidas correctamente",
                    "message": "Estados obtenidas correctamente",
                    "data": dic_estado,
                }
            )
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(f"Error al listar el estado: {str(e)}")
            dic_response.update(
                {"message": "Error al listar el estado", "data": str(e)}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

# -> CRUD de Unidad de Medida

@api_view(["GET"])
@transaction.atomic
def listar_unidadmedida(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Unidad de medida no encontradas",
        "message_user": "Unidad de medida no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id,
                        nombre
                    FROM UnidadMedida
                    WHERE estado_id IN (1, 2)
                    ORDER BY id DESC
                    """
                )
                dic_unidadmedida = ConvertirQueryADiccionarioDato(cursor)
                cursor.close()

            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Unidad de medida obtenidas correctamente",
                    "message": "Unidad de medida obtenidas correctamente",
                    "data": dic_unidadmedida,
                }
            )
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(f"Error al listar la unidad de medida: {str(e)}")
            dic_response.update(
                {"message": "Error al listar la unidad de medida", "data": str(e)}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(["POST"])
@transaction.atomic
def crear_unidadmedida(request):

    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al crear la unidad de medida",
        "message_user": "Error al crear la unidad de medida",
        "data": [],
    }

    if request.method == "POST":
        try:
            
            data = json.loads(request.body)
            data["estado"] = 1 
            data["fecha_creacion"] = datetime.now()
            data["fecha_modificacion"] = datetime.now()

            serializer = UnidadMedidaSerializer(data=data)

            if serializer.is_valid():
            
                with connection.cursor() as cursor:

                    nombre = data["nombre"]
                    
                    cursor.execute(
                        "SELECT nombre FROM UnidadMedida WHERE (nombre='{0}') and estado_id IN (1, 2)".format(nombre)
                    )

                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {"message_user": "Ya existe una Unidad de Medida con el mismo Nombre", "message": "Ya hay un dato existente."}
                        )
                        return JsonResponse(dic_response, status=400)
                
                    cursor.close()

                serializer.save()
                
                dic_response.update(
                    {
                        "code": 201,
                        "status": "success",
                        "message_user": "Unidad Medida creado exitosamente",
                        "message": "Unidad Medida  creado exitosamente",
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

            logger.error(f"Error inesperado al crear la unidad de medida: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)
        
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(["PUT"])
@transaction.atomic
def actualizar_unidadmedida(request, id):

    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al actualizar la unidad de medida",
        "message_user": "Error al actualizar la unidad de medida",
        "data": [],
    }

    if request.method == "PUT":
        try:
            
            data = json.loads(request.body)
            
            data["fecha_modificacion"] = datetime.now()

            try:
                queryset = UnidadMedida.objects.using('default').get(id=id)
            except UnidadMedida.DoesNotExist:
                
                return JsonResponse(dic_response, safe=False, status=status.HTTP_404_NOT_FOUND)

            serializer = UnidadMedidaSerializer(queryset, data=data)

            if serializer.is_valid():

                with connection.cursor() as cursor:

                    nombre = data["nombre"]
                    estado = data["estado"]
                    
                    cursor.execute("SELECT nombre FROM UnidadMedida WHERE (nombre='{0}') and estado_id = {1} and id <> {2}".format(nombre, estado, id))
                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {"message_user": "Ya existe una unidad de medida con el mismo nombre", "message": "Ya hay un dato existente."}
                        )
                        return JsonResponse(dic_response, status=400)

                    cursor.close()

                serializer.save()
                
                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Unidad de medida actualizado exitosamente",
                        "message": "Unidad de medida actualizado exitosamente",
                        "data": serializer.data
                    }
                )

                return JsonResponse([], safe=False, status=status.HTTP_200_OK)

            dic_response.update(
                {
                    "message_user": "Datos inválidos.",
                    "data": serializer.errors,
                }
            )
            return JsonResponse(dic_response, status=400)

        except Exception as e:

            logger.error(f"Error inesperado al actualizar la unidad de medida: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@transaction.atomic
def eliminar_unidadmedida(request, id):

    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al eliminar la unidad de medida",
        "message_user": "Error al eliminar la unidad de medida",
        "data": [],
    }

    if request.method == "DELETE":
        try:

            data = {"estado": 3}        

            try:
                queryset = UnidadMedida.objects.using('default').get(id=id)

                queryset.estado = Estado.objects.using('default').get(id=data["estado"])
                queryset.fecha_modificacion = datetime.now()
                
                queryset.save()

                serializer = UnidadMedidaSerializer(queryset)

                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Unidad de medida eliminado lógicamente",
                        "message": "Unidad de medida eliminado lógicamente",
                        "data": serializer.data,
                    }
                )

                return JsonResponse([], safe=False, status=status.HTTP_200_OK)

            except UnidadMedida.DoesNotExist:
                return JsonResponse(dic_response, safe=False, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar la unidad de medida: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_200_OK)


# -> CRUD de Conversion Unidad de Medida
@api_view(["GET"])
@transaction.atomic
def listar_conversionunidadmedida(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Conversiones Unidad de medida no encontradas",
        "message_user": "Conversiones Unidad de medida no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id,
                        nombre
                    FROM ConversionUnidadMedida 
                    WHERE estado_id IN (1, 2)
                    ORDER BY id DESC
                    """
                )
                dic_conversionunidadmedida = ConvertirQueryADiccionarioDato(cursor)
                cursor.close()

            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Conversiones Unidad de medida obtenidas correctamente",
                    "message": "Conversiones Unidad de medida obtenidas correctamente",
                    "data": dic_conversionunidadmedida,
                }
            )
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(f"Error al listar las Conversiones unidad de medida: {str(e)}")
            dic_response.update(
                {"message": "Error al listar las Conversiones unidad de medida", "data": str(e)}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(["POST"])
@transaction.atomic
def crear_conversionunidadmedida(request):

    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al crear la conversion de unidad de medida",
        "message_user": "Error al crear la conversion de unidad de medida",
        "data": [],
    }

    if request.method == "POST":
        try:
            
            data = json.loads(request.body)
            data["estado"] = 1 
            data["fecha_creacion"] = datetime.now()
            data["fecha_modificacion"] = datetime.now()

            serializer = ConversionUnidadMedidaSerializer(data=data)

            if serializer.is_valid():
            
                with connection.cursor() as cursor:

                    nombre = data["nombre"]
                    
                    cursor.execute(
                        "SELECT nombre FROM ConversionUnidadMedida WHERE (nombre='{0}') and estado_id IN (1, 2)".format(nombre)
                    )

                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {"message_user": "Ya existe una Conversion de Unidad de Medida con el mismo nombre", "message": "Ya hay un dato existente."}
                        )
                        return JsonResponse(dic_response, status=400)
                
                    cursor.close()

                serializer.save()
                
                dic_response.update(
                    {
                        "code": 201,
                        "status": "success",
                        "message_user": "Conversion de Unidad Medida creado exitosamente",
                        "message": "Conversion de Unidad Medida  creado exitosamente",
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

            logger.error(f"Error inesperado al crear la Conversion de Unidad de medida: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)
        
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(["PUT"])
@transaction.atomic
def actualizar_conversionunidadmedida(request, id):

    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al actualizar la conversion de unidad de medida",
        "message_user": "Error al actualizar la conversion de unidad de medida",
        "data": [],
    }

    if request.method == "PUT":
        try:
            
            data = json.loads(request.body)
            
            data["fecha_modificacion"] = datetime.now()

            try:
                queryset = ConversionUnidadMedida.objects.using('default').get(id=id)
            except ConversionUnidadMedida.DoesNotExist:
                
                return JsonResponse(dic_response, safe=False, status=status.HTTP_404_NOT_FOUND)

            serializer = ConversionUnidadMedidaSerializer(queryset, data=data)

            if serializer.is_valid():

                with connection.cursor() as cursor:

                    nombre = data["nombre"]
                    estado = data["estado"]
                    
                    cursor.execute("SELECT nombre FROM ConversionUnidadMedida WHERE (nombre='{0}') and estado_id = {1} and id <> {2}".format(nombre, estado, id))
                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {"message_user": "Ya existe una conversion de unidad de medida con el mismo nombre", "message": "Ya hay un dato existente."}
                        )
                        return JsonResponse(dic_response, status=400)

                    cursor.close()

                serializer.save()
                
                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Conversion de Unidad de medida actualizado exitosamente",
                        "message": "Conversion de Unidad de medida actualizado exitosamente",
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

            logger.error(f"Error inesperado al actualizar la conversion de unidad de medida: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@transaction.atomic
def eliminar_conversionunidadmedida(request, id):

    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al eliminar la unidad de medida",
        "message_user": "Error al eliminar la unidad de medida",
        "data": [],
    }

    if request.method == "DELETE":
        try:

            data = {"estado": 3}        

            try:
                queryset = ConversionUnidadMedida.objects.using('default').get(id=id)

                queryset.estado = Estado.objects.using('default').get(id=data["estado"])
                queryset.fecha_modificacion = datetime.now()
                
                queryset.save()

                serializer = ConversionUnidadMedidaSerializer(queryset)

                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Conversion de Unidad de medida eliminado lógicamente",
                        "message": "Conversion de Unidad de medida eliminado lógicamente",
                        "data": serializer.data,
                    }
                )

                return JsonResponse(dic_response, status=200)

            except ConversionUnidadMedida.DoesNotExist:
                return JsonResponse(dic_response, safe=False, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar la conversion de unidad de medida: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

# -> CRUD de Mercado
@api_view(["GET"])
@transaction.atomic
def listar_mercados(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Mercados no encontradas",
        "message_user": "Mercados no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id,
                        nombre
                    FROM Mercado 
                    WHERE estado_id IN (1, 2)
                    ORDER BY id DESC
                    """
                )
                dic_mercado = ConvertirQueryADiccionarioDato(cursor)
                cursor.close()

            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Mercados obtenidos correctamente",
                    "message": "Mercados obtenidos correctamente",
                    "data": dic_mercado,
                }
            )
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(f"Error al listar los Mercados: {str(e)}")
            dic_response.update(
                {"message": "Error al listar los Mercados", "data": str(e)}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(["POST"])
@transaction.atomic
def crear_mercado(request):

    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al crear el mercado",
        "message_user": "Error al crear el mercado",
        "data": [],
    }

    if request.method == "POST":
        try:
            
            data = json.loads(request.body)
            data["estado"] = 1 
            data["fecha_creacion"] = datetime.now()
            data["fecha_modificacion"] = datetime.now()

            serializer = MercadoSerializer(data=data)

            if serializer.is_valid():
            
                with connection.cursor() as cursor:

                    nombre = data["nombre"]
                    
                    cursor.execute(
                        "SELECT nombre FROM Mercado WHERE (nombre='{0}') and estado_id IN (1, 2)".format(nombre)
                    )

                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {"message_user": "Ya existe un Mercado con el mismo nombre", "message": "Ya hay un dato existente."}
                        )
                        return JsonResponse(dic_response, status=400)
                
                    cursor.close()

                serializer.save()
                
                dic_response.update(
                    {
                        "code": 201,
                        "status": "success",
                        "message_user": "Mercado creado exitosamente",
                        "message": "Mercado creado exitosamente",
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

            logger.error(f"Error inesperado al crear el Mercado: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)
        
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(["PUT"])
@transaction.atomic
def actualizar_mercado(request, id):

    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al actualizar el mercado",
        "message_user": "Error al actualizar el mercado",
        "data": [],
    }

    if request.method == "PUT":
        try:
            
            data = json.loads(request.body)
            
            data["fecha_modificacion"] = datetime.now()

            try:
                queryset = Mercado.objects.using('default').get(id=id)
            except Mercado.DoesNotExist:
                
                return JsonResponse(dic_response, safe=False, status=status.HTTP_404_NOT_FOUND)

            serializer = MercadoSerializer(queryset, data=data)

            if serializer.is_valid():

                with connection.cursor() as cursor:

                    nombre = data["nombre"]
                    estado = data["estado"]
                    
                    cursor.execute("SELECT nombre FROM Mercado WHERE (nombre='{0}') and estado_id = {1} and id <> {2}".format(nombre, estado, id))
                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {"message_user": "Ya existe un Mercado con el mismo nombre", "message": "Ya hay un dato existente."}
                        )
                        return JsonResponse(dic_response, status=400)

                    cursor.close()

                serializer.save()
                
                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Mercado actualizado exitosamente",
                        "message": "Mercado actualizado exitosamente",
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

            logger.error(f"Error inesperado al actualizar el Mercado: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@transaction.atomic
def eliminar_mercado(request, id):
    
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al eliminar el mercado",
        "message_user": "Error al eliminar el mercado",
        "data": [],
    }

    if request.method == "DELETE":
        try:

            data = {"estado": 3}        

            try:
                queryset = Mercado.objects.using('default').get(id=id)

                queryset.estado = Estado.objects.using('default').get(id=data["estado"])
                queryset.fecha_modificacion = datetime.now()
                
                queryset.save()

                serializer = MercadoSerializer(queryset)

                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Mercado eliminado lógicamente",
                        "message": "Mercado eliminado lógicamente",
                        "data": serializer.data,
                    }
                )

                return JsonResponse(dic_response, status=200)

            except Mercado.DoesNotExist:
                return JsonResponse(dic_response, safe=False, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar el mercado: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_200_OK)
    
    
# -> CRUD de Pais
@api_view(["GET"])
@transaction.atomic
def listar_paises(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Paises no encontradas",
        "message_user": "Paises no encontradas",
        "data": [],
    }
    if request.method == "GET":
        try:

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id,
                        nombre
                    FROM Pais 
                    WHERE estado_id IN (1, 2)
                    ORDER BY id DESC
                    """
                )
                dic_pais = ConvertirQueryADiccionarioDato(cursor)
                cursor.close()

            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Paises obtenidos correctamente",
                    "message": "Paises obtenidos correctamente",
                    "data": dic_pais,
                }
            )
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(f"Error al listar los Paises: {str(e)}")
            dic_response.update(
                {"message": "Error al listar los Paises", "data": str(e)}
            )
            return JsonResponse(dic_response, status=500)
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(["POST"])
@transaction.atomic
def crear_pais(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al crear el pais",
        "message_user": "Error al crear el pais",
        "data": [],
    }

    if request.method == "POST":
        try:
            
            data = json.loads(request.body)
            data["estado"] = 1 
            data["fecha_creacion"] = datetime.now()
            data["fecha_modificacion"] = datetime.now()

            serializer = PaisSerializer(data=data)

            if serializer.is_valid():
            
                with connection.cursor() as cursor:

                    nombre = data["nombre"]
                    
                    cursor.execute(
                        "SELECT nombre FROM Pais WHERE (nombre='{0}') and estado_id IN (1, 2)".format(nombre)
                    )

                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {"message_user": "Ya existe un Pais con el mismo nombre", "message": "Ya hay un dato existente."}
                        )
                        return JsonResponse(dic_response, status=400)
                
                    cursor.close()

                serializer.save()
                
                dic_response.update(
                    {
                        "code": 201,
                        "status": "success",
                        "message_user": "Pais creado exitosamente",
                        "message": "Pais creado exitosamente",
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

            logger.error(f"Error inesperado al crear el Pais: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)
        
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(["PUT"])
@transaction.atomic
def actualizar_pais(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al actualizar el pais",
        "message_user": "Error al actualizar el pais",
        "data": [],
    }

    if request.method == "PUT":
        try:
            
            data = json.loads(request.body)
            
            data["fecha_modificacion"] = datetime.now()

            try:
                queryset = Pais.objects.using('default').get(id=id)
            except Pais.DoesNotExist:
                
                return JsonResponse(dic_response, safe=False, status=status.HTTP_404_NOT_FOUND)

            serializer = PaisSerializer(queryset, data=data)

            if serializer.is_valid():

                with connection.cursor() as cursor:

                    nombre = data["nombre"]
                    estado = data["estado"]
                    
                    cursor.execute("SELECT nombre FROM Pais WHERE (nombre='{0}') and estado_id = {1} and id <> {2}".format(nombre, estado, id))
                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {"message_user": "Ya existe un Pais con el mismo nombre", "message": "Ya hay un dato existente."}
                        )
                        return JsonResponse(dic_response, status=400)

                    cursor.close()

                serializer.save()
                
                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Pais actualizado exitosamente",
                        "message": "Pais actualizado exitosamente",
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

            logger.error(f"Error inesperado al actualizar el Pais: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@transaction.atomic
def eliminar_pais(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al eliminar el pais",
        "message_user": "Error al eliminar el pais",
        "data": [],
    }

    if request.method == "DELETE":
        try:

            data = {"estado": 3}        

            try:
                queryset = Pais.objects.using('default').get(id=id)

                queryset.estado = Estado.objects.using('default').get(id=data["estado"])
                queryset.fecha_modificacion = datetime.now()
                
                queryset.save()

                serializer = PaisSerializer(queryset)

                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Pais eliminado lógicamente",
                        "message": "Pais eliminado lógicamente",
                        "data": serializer.data,
                    }
                )

                return JsonResponse(dic_response, status=200)

            except Pais.DoesNotExist:
                return JsonResponse(dic_response, safe=False, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar el pais: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_200_OK)


# -> CRUD de Departamento
@api_view(["GET"])
@transaction.atomic
def listar_departamentos(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Departamentos no encontradas",
        "message_user": "Departamentos no encontradas",
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
                        pais_id
                    FROM Departamento 
                    WHERE estado_id IN (1, 2)
                    ORDER BY id DESC
                    """
                )
                dic_departamento = ConvertirQueryADiccionarioDato(cursor)
                cursor.close()

            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Departamentos obtenidos correctamente",
                    "message": "Departamentos obtenidos correctamente",
                    "data": dic_departamento,
                }
            )
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(f"Error al listar los departamentos: {str(e)}")
            dic_response.update(
                {"message": "Error al listar los departamentos", "data": str(e)}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_200_OK)


api_view(["POST"])
@transaction.atomic
def crear_departamento(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al crear el departamento",
        "message_user": "Error al crear el departamento",
        "data": [],
    }

    if request.method == "POST":
        try:
            
            data = json.loads(request.body)
            data["estado"] = 1 
            data["fecha_creacion"] = datetime.now()
            data["fecha_modificacion"] = datetime.now()

            serializer = DepartamentoSerializer(data=data)

            if serializer.is_valid():
            
                with connection.cursor() as cursor:

                    nombre = data["nombre"]
                    
                    cursor.execute(
                        "SELECT nombre FROM Departamento WHERE (nombre='{0}') and estado_id IN (1, 2)".format(nombre)
                    )

                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {"message_user": "Ya existe un Departamento con el mismo nombre", "message": "Ya hay un dato existente."}
                        )
                        return JsonResponse(dic_response, status=400)
                
                    cursor.close()

                serializer.save()
                
                dic_response.update(
                    {
                        "code": 201,
                        "status": "success",
                        "message_user": "Departamento creado exitosamente",
                        "message": "Departamento creado exitosamente",
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

            logger.error(f"Error inesperado al crear el departamento: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)
        
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)


@api_view(["PUT"])
@transaction.atomic
def actualizar_departamento(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al actualizar el departamento",
        "message_user": "Error al actualizar el departamento",
        "data": [],
    }
    if request.method == "PUT":
        try:
            
            data = json.loads(request.body)
            
            data["fecha_modificacion"] = datetime.now()

            try:
                queryset = Departamento.objects.using('default').get(id=id)
            except Departamento.DoesNotExist:
                
                return JsonResponse(dic_response, safe=False, status=status.HTTP_404_NOT_FOUND)

            serializer = DepartamentoSerializer(queryset, data=data)

            if serializer.is_valid():

                with connection.cursor() as cursor:

                    nombre = data["nombre"]
                    estado = data["estado"]
                    
                    cursor.execute("SELECT nombre FROM Departamento WHERE (nombre='{0}') and estado_id = {1} and id <> {2}".format(nombre, estado, id))
                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {"message_user": "Ya existe un departamento con el mismo nombre", "message": "Ya hay un dato existente."}
                        )
                        return JsonResponse(dic_response, status=400)

                    cursor.close()

                serializer.save()
                
                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Departamento actualizado exitosamente",
                        "message": "Departamento actualizado exitosamente",
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

            logger.error(f"Error inesperado al actualizar el departamento: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)
        
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@transaction.atomic
def eliminar_departamento(request, id):
    
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al eliminar el departamento",
        "message_user": "Error al eliminar el departamento",
        "data": [],
    }

    if request.method == "DELETE":
        try:

            data = {"estado": 3}        

            try:
                queryset = Departamento.objects.using('default').get(id=id)

                queryset.estado = Estado.objects.using('default').get(id=data["estado"])
                queryset.fecha_modificacion = datetime.now()
                
                queryset.save()

                serializer = DepartamentoSerializer(queryset)

                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Departamento eliminado lógicamente",
                        "message": "Departamento eliminado lógicamente",
                        "data": serializer.data,
                    }
                )

                return JsonResponse(dic_response, status=200)

            except Departamento.DoesNotExist:
                return JsonResponse(dic_response, safe=False, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar el departamento: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)   
    
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)
    
# -> CRUD de Provincia
@api_view(["GET"])
@transaction.atomic
def listar_provincias(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Provincias no encontradas",
        "message_user": "Provincias no encontradas",
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
                        departamento_id
                    FROM Provincia 
                    WHERE estado_id IN (1, 2)
                    ORDER BY id DESC
                    """
                )
                dic_provincias = ConvertirQueryADiccionarioDato(cursor)
                cursor.close()

            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Provincias obtenidos correctamente",
                    "message": "Provincias obtenidos correctamente",
                    "data": dic_provincias,
                }
            )
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(f"Error al listar las Provincias: {str(e)}")
            dic_response.update(
                {"message": "Error al listar las Provincias", "data": str(e)}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(["POST"])
@transaction.atomic
def crear_provincia(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al crear la provincia",
        "message_user": "Error al crear la provincia",
        "data": [],
    }

    if request.method == "POST":
        try:
            
            data = json.loads(request.body)
            data["estado"] = 1 
            data["fecha_creacion"] = datetime.now()
            data["fecha_modificacion"] = datetime.now()

            serializer = ProvinciaSerializer(data=data)

            if serializer.is_valid():
            
                with connection.cursor() as cursor:

                    nombre = data["nombre"]
                    
                    cursor.execute(
                        "SELECT nombre FROM Provincia WHERE (nombre='{0}') and estado_id IN (1, 2)".format(nombre)
                    )

                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {"message_user": "Ya existe una provincia con el mismo nombre", "message": "Ya hay un dato existente."}
                        )
                        return JsonResponse(dic_response, status=400)
                
                    cursor.close()

                serializer.save()
                
                dic_response.update(
                    {
                        "code": 201,
                        "status": "success",
                        "message_user": "Provincia creado exitosamente",
                        "message": "Provincia creado exitosamente",
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

            logger.error(f"Error inesperado al crear la provincia: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)
        
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(["PUT"])
@transaction.atomic
def actualizar_provincia(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al actualizar la provincia",
        "message_user": "Error al actualizar la provincia",
        "data": [],
    }

    if request.method == "PUT":
        try:
            
            data = json.loads(request.body)
            
            data["fecha_modificacion"] = datetime.now()

            try:
                queryset = Provincia.objects.using('default').get(id=id)
            except Provincia.DoesNotExist:
                
                return JsonResponse(dic_response, safe=False, status=status.HTTP_404_NOT_FOUND)

            serializer = ProvinciaSerializer(queryset, data=data)

            if serializer.is_valid():

                with connection.cursor() as cursor:

                    nombre = data["nombre"]
                    estado = data["estado"]
                    
                    cursor.execute("SELECT nombre FROM Provincia WHERE (nombre='{0}') and estado_id = {1} and id <> {2}".format(nombre, estado, id))
                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {"message_user": "Ya existe una provincia con el mismo nombre", "message": "Ya hay un dato existente."}
                        )
                        return JsonResponse(dic_response, status=400)

                    cursor.close()

                serializer.save()
                
                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Provincia actualizado exitosamente",
                        "message": "Provincia actualizado exitosamente",
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

            logger.error(f"Error inesperado al actualizar la provincia: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@transaction.atomic
def eliminar_provincia(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al eliminar la provincia",
        "message_user": "Error al eliminar la provincia",
        "data": [],
    }
    if request.method == "DELETE":
        try:

            data = {"estado": 3}        

            try:
                queryset = Provincia.objects.using('default').get(id=id)

                queryset.estado = Estado.objects.using('default').get(id=data["estado"])
                queryset.fecha_modificacion = datetime.now()
                
                queryset.save()

                serializer = ProvinciaSerializer(queryset)

                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Provincia eliminado lógicamente",
                        "message": "Provincia eliminado lógicamente",
                        "data": serializer.data,
                    }
                )

                return JsonResponse(dic_response, status=200)

            except Provincia.DoesNotExist:
                return JsonResponse(dic_response, safe=False, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar la provincia: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
        
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)



# -> CRUD de Distrito
@api_view(["GET"])
@transaction.atomic
def listar_distritos(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Distritos no encontradas",
        "message_user": "Distritos no encontradas",
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
                        provincia_id
                    FROM Distrito 
                    WHERE estado_id IN (1, 2)
                    ORDER BY id DESC
                    """
                )
                dic_distritos = ConvertirQueryADiccionarioDato(cursor)
                cursor.close()

            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Distritos obtenidos correctamente",
                    "message": "Distritos obtenidos correctamente",
                    "data": dic_distritos,
                }
            )
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(f"Error al listar los Distritos: {str(e)}")
            dic_response.update(
                {"message": "Error al listar los Distritos", "data": str(e)}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_200_OK)


@api_view(["POST"])
@transaction.atomic
def crear_distrito(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al crear el distrito",
        "message_user": "Error al crear el distrito",
        "data": [],
    }

    if request.method == "POST":
        try:
            
            data = json.loads(request.body)
            data["estado"] = 1 
            data["fecha_creacion"] = datetime.now()
            data["fecha_modificacion"] = datetime.now()

            serializer = DistritoSerializer(data=data)

            if serializer.is_valid():
            
                with connection.cursor() as cursor:

                    nombre = data["nombre"]
                    
                    cursor.execute(
                        "SELECT nombre FROM Distrito WHERE (nombre='{0}') and estado_id IN (1, 2)".format(nombre)
                    )

                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {"message_user": "Ya existe un distrito con el mismo nombre", "message": "Ya hay un dato existente."}
                        )
                        return JsonResponse(dic_response, status=400)
                
                    cursor.close()

                serializer.save()
                
                dic_response.update(
                    {
                        "code": 201,
                        "status": "success",
                        "message_user": "Distrito creado exitosamente",
                        "message": "Distrito creado exitosamente",
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

            logger.error(f"Error inesperado al crear el distrito: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)
        
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(["PUT"])
@transaction.atomic
def actualizar_distrito(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al actualizar el distrito",
        "message_user": "Error al actualizar el distrito",
        "data": [],
    }

    if request.method == "PUT":
        try:
            
            data = json.loads(request.body)
            
            data["fecha_modificacion"] = datetime.now()

            try:
                queryset = Distrito.objects.using('default').get(id=id)
            except Distrito.DoesNotExist:
                
                return JsonResponse(dic_response, safe=False, status=status.HTTP_404_NOT_FOUND)

            serializer = DistritoSerializer(queryset, data=data)

            if serializer.is_valid():

                with connection.cursor() as cursor:

                    nombre = data["nombre"]
                    estado = data["estado"]
                    
                    cursor.execute("SELECT nombre FROM Distrito WHERE (nombre='{0}') and estado_id = {1} and id <> {2}".format(nombre, estado, id))
                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {"message_user": "Ya existe un distrito con el mismo nombre", "message": "Ya hay un dato existente."}
                        )
                        return JsonResponse(dic_response, status=400)

                    cursor.close()

                serializer.save()
                
                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Distrito actualizado exitosamente",
                        "message": "Distrito actualizado exitosamente",
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

            logger.error(f"Error inesperado al actualizar el distrito: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_200_OK)


api_view(["DELETE"])
@transaction.atomic
def eliminar_distrito(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al eliminar el distrito",
        "message_user": "Error al eliminar el distrito",
        "data": [],
    }

    if request.method == "DELETE":
        try:

            data = {"estado": 3}        

            try:
                queryset = Distrito.objects.using('default').get(id=id)

                queryset.estado = Estado.objects.using('default').get(id=data["estado"])
                queryset.fecha_modificacion = datetime.now()
                
                queryset.save()

                serializer = DistritoSerializer(queryset)

                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Distrito eliminado lógicamente",
                        "message": "Distrito eliminado lógicamente",
                        "data": serializer.data,
                    }
                )

                return JsonResponse(dic_response, status=200)

            except Distrito.DoesNotExist:
                return JsonResponse(dic_response, safe=False, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar el distrito: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)


api_view(["GET"])
@transaction.atomic
def listar_localidadcaserio(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Localidad - Caserio no encontradas",
        "message_user": "Localidad - Caserio no encontradas",
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
                        distrito_id
                    FROM LocalidadCaserio 
                    WHERE estado_id IN (1, 2)
                    ORDER BY id DESC
                    """
                )
                dic_localidadcaserio = ConvertirQueryADiccionarioDato(cursor)
                cursor.close()

            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Localidad - Caserio obtenidos correctamente",
                    "message": "Localidad - Caserio obtenidos correctamente",
                    "data": dic_localidadcaserio,
                }
            )
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(f"Error al listar los LocalidadCaserio: {str(e)}")
            dic_response.update(
                {"message": "Error al listar los LocalidadCaserio", "data": str(e)}
            )
            return JsonResponse(dic_response, status=500)   
    
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(["POST"])
@transaction.atomic
def crear_localidadcaserio(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al crear la localidad - caserio",
        "message_user": "Error al crear la localidad - caserio",
        "data": [],
    }

    if request.method == "POST":
        try:
            
            data = json.loads(request.body)
            data["estado"] = 1 
            data["fecha_creacion"] = datetime.now()
            data["fecha_modificacion"] = datetime.now()

            serializer = LocalidadCaserioSerializer(data=data)

            if serializer.is_valid():
            
                with connection.cursor() as cursor:

                    nombre = data["nombre"]
                    
                    cursor.execute(
                        "SELECT nombre FROM LocalidadCaserio WHERE (nombre='{0}') and estado_id IN (1, 2)".format(nombre)
                    )

                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {"message_user": "Ya existe una localidad - caserio con el mismo nombre", "message": "Ya hay un dato existente."}
                        )
                        return JsonResponse(dic_response, status=400)
                cursor.close()
                serializer.save()
                dic_response.update(
                    {
                        "code": 201,
                        "status": "success",
                        "message_user": "Localidad - Caserio creado exitosamente",
                        "message": "Localidad - Caserio creado exitosamente",
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
            logger.error(f"Error inesperado al crear la localidad - caserio: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)

@api_view(["PUT"])
@transaction.atomic
def actualizar_localidadcaserio(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al actualizar la localidad - caserio",
        "message_user": "Error al actualizar la localidad - caserio",
        "data": [],
    }

    if request.method == "PUT":
        try:
            
            data = json.loads(request.body)
            
            data["fecha_modificacion"] = datetime.now()

            try:
                queryset = LocalidadCaserio.objects.using('default').get(id=id)
            except LocalidadCaserio.DoesNotExist:
                
                return JsonResponse(dic_response, safe=False, status=status.HTTP_404_NOT_FOUND)

            serializer = LocalidadCaserioSerializer(queryset, data=data)

            if serializer.is_valid():

                with connection.cursor() as cursor:

                    nombre = data["nombre"]
                    estado = data["estado"]
                    
                    cursor.execute("SELECT nombre FROM LocalidadCaserio WHERE (nombre='{0}') and estado_id = {1} and id <> {2}".format(nombre, estado, id))
                    if len(cursor.fetchall()) > 0:
                        dic_response.update(
                            {"message_user": "Ya existe una localidad - caserio con el mismo nombre", "message": "Ya hay un dato existente."}
                        )
                        return JsonResponse(dic_response, status=400)

                    cursor.close()
                serializer.save()
                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Localidad - Caserio actualizado exitosamente",
                        "message": "Localidad - Caserio actualizado exitosamente",
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
            logger.error(f"Error inesperado al actualizar la localidad - caserio: {str(e)}")
            dic_response.update(
                {"message_user": "Error inesperado", "data": {"error": str(e)}}
            )
            return JsonResponse(dic_response, status=500)
        
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@transaction.atomic
def eliminar_localidadcaserio(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al eliminar la localidad - caserio",
        "message_user": "Error al eliminar la localidad - caserio",
        "data": [],
    }

    if request.method == "DELETE":
        try:

            data = {"estado": 3}        

            try:
                queryset = LocalidadCaserio.objects.using('default').get(id=id)

                queryset.estado = Estado.objects.using('default').get(id=data["estado"])
                queryset.fecha_modificacion = datetime.now()
                
                queryset.save()

                serializer = LocalidadCaserioSerializer(queryset)

                dic_response.update(
                    {
                        "code": 200,
                        "status": "success",
                        "message_user": "Localidad - Caserio eliminado lógicamente",
                        "message": "Localidad - Caserio eliminado lógicamente",
                        "data": serializer.data,
                    }
                )

                return JsonResponse(dic_response, status=200)

            except LocalidadCaserio.DoesNotExist:
                return JsonResponse(dic_response, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error inesperado al eliminar la localidad - caserio: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)


