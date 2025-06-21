from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.conf import settings
from django.template.defaulttags import url
from django.urls import path

from .views import *

# Definición de las rutas URL para la API de clientes
urlpatterns = [
    # Rutas para la API de TIPOS DEMANDAS
    path("tiposdemandas/", listar_tiposdemandas, name="listar_tiposdemandas"),
    # Rutas para la API de DEMANDA PRODUCTOS AGROPECUARIOS
    path("demandas/<int:id>/", listar_demandas, name="listar_demandas"),
    path("demandas/crear/", crear_demandas, name="crear_demandas"),
    path("demandas/actualizar/<int:id>/", actualizar_demandas, name="actualizar_demandas"),
    path("demandas/eliminar/<int:id>/", eliminar_demandas, name="eliminar_demandas"),
    path("demandas/eliminacion-masiva/", eliminar_demandas_masivas, name="eliminar_demandas_masivas"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)