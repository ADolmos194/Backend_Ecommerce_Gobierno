from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.conf import settings
from django.template.defaulttags import url
from django.urls import path

from .views import *

# Definición de las rutas URL para la API de clientes
urlpatterns = [
    
    
    # URL -> Precios Mercado Mayorista Minorista # 
    path('preciosmercadomayoristaminorista/', listar_PreciosMercadoMayoristaMinorista, name='listar_precios_mercado_mayorista_minorista'),
    path('preciosmercadomayoristaminorita/crear/', crear_PreciosMercadoMayoristaMinorista, name='crear_precios_mercado_mayorista_minorista'),
    path('preciosmercadomayoristaminorita/actualizar/<int:id>/', actualizar_PreciosMercadoMayoristaMinorista, name='actualizar_precios_mercado_mayorista_minorista'),
    path('preciosmercadomayoristaminorita/eliminar/<int:id>/', eliminar_PreciosMercadoMayoristaMinorista, name='eliminar_precios_mercado_mayorista_minorista'),
    
    # URL -> Precios Ciudades #
    
    path('preciosciudades/', listar_PrecioCiudades, name='listar_PrecioCiudades'),
    path('preciosciudades/crear/', crear_PrecioCiudades, name='crear_PrecioCiudades'),
    path('preciosciudades/actualizar/<int:id>/', actualizar_PrecioCiudades, name='actualizar_PrecioCiudades'),
    path('preciosciudades/eliminar/<int:id>/', eliminar_PrecioCiudades, name='eliminar_PrecioCiudades'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)