from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.conf import settings
from django.template.defaulttags import url
from django.urls import path

from .views import *

# Definición de las rutas URL para la API de clientes
urlpatterns = [

    # Rutas para la API de DEMANDA PRODUCTOS AGROPECUARIOS
    path("demandaproductosagropecuarios/", listar_demandaproductosagropecuarios, name="listar_demandaproductosagropecuarios"),
    path("demandaproductosagropecuarios/crear/", crear_demandaproductosagropecuarios, name="crear_demandaproductosagropecuarios"),
    path("demandaproductosagropecuarios/actualizar/<int:id>/", actualizar_demandaproductosagropecuarios, name="actualizar_demandaproductosagropecuarios"),
    path("demandaproductosagropecuarios/eliminar/<int:id>/", eliminar_demandaproductosagropecuarios, name="eliminar_demandaproductosagropecuarios"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)