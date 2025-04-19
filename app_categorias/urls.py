from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.conf import settings
from django.template.defaulttags import url
from django.urls import path

# Importación de las vistas que serán utilizadas en las URLs
from .views import *

# Definición de las URLs de la aplicación
urlpatterns = [
    path('tipoproducto/', listar_tipoproducto, name='listar_tipoproducto'),
    path('tipoproducto/crear/', crear_tipoproducto, name='crear_tipoproducto'),
    path('tipoproducto/actualizar/<int:id>/', actualizar_producto, name='actualizar_producto'),
    path('tipoproducto/eliminar/<int:id>/', eliminar_tipoproducto, name='eliminar_tipoproducto'),
    
    path('producto/', listar_producto, name='listar_producto'),
    path('producto/crear/', crear_producto, name='crear_producto'),
    path('producto/actualizar/<int:id>/', actualizar_producto, name='actualizar_producto'),
    path('producto/eliminar/<int:id>/', eliminar_producto, name='eliminar_producto'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)