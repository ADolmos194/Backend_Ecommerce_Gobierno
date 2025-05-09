from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.conf import settings
from django.template.defaulttags import url
from django.urls import path

# Importación de las vistas que serán utilizadas en las URLs
from .views import *

# Definición de las URLs de la aplicación
urlpatterns = [
    
    path('verificacionusuariosistema/', verificacion_usuariosistema, name='verificacion_usuariosistema'),
    path('usuariosistema/', listar_usuariosistema, name='listar_usuariosistema'),
    path('usuariosistema/crear/', crear_usuariosistema, name='crear_usuariosistema'),

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)