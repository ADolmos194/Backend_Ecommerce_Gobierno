from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.conf import settings
from django.template.defaulttags import url
from django.urls import path

from .views import *

# Definición de las rutas URL para la API de clientes
urlpatterns = [

    # Rutas para la API de DEMANDA PRODUCTOS AGROPECUARIOS
    path("ofertas/<int:id>/", listar_ofertas, name="listar_ofertas"),
    path("ofertas/crear/", crear_ofertas, name="crear_demcrear_ofertasandas"),
    path("ofertas/actualizar/<int:id>/", actualizar_ofertas, name="actualizar_ofertas"),
    path("ofertas/eliminar/<int:id>/", eliminar_ofertas, name="eliminar_ofertas"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)