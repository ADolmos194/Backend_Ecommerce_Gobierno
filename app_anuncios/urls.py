from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.conf import settings
from django.template.defaulttags import url
from django.urls import path

# Importación de las vistas que serán utilizadas en las URLs
from .views import *

# Definición de las URLs de la aplicación
urlpatterns = [

    #api url tipo de anuncio    
    path("tipoanuncio/", listar_tipoanuncio, name="listar_tipoanuncio"),
    path("tipoanuncio/crear/", crear_tipoanuncio, name="crear_tipoanuncio"),
    path("tipoanuncio/actualizar/<int:id>/", actualizar_tipoanuncio, name="actualizar_tipoanuncio"),
    path("tipoanuncio/eliminar/<int:id>/", eliminar_tipoanuncio, name="eliminar_tipoanuncio"),

    #api url de anuncion compra-venta 
    

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)