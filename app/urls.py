from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.conf import settings
from django.template.defaulttags import url
from django.urls import path

# Importación de las vistas que serán utilizadas en las URLs
from .views import *

# Definición de las URLs de la aplicación
urlpatterns = [
    path('estado/', listar_estado, name='listar_estado'),
    
    #---> URL Unidad Medida 
    path('unidadmedida/', listar_unidadmedida, name='listar_unidadmedida'),
    path('unidadmedida/crear/', crear_unidadmedida, name='crear_unidadmedida'),
    path('unidadmedida/actualizar/<int:id>/', actualizar_unidadmedida, name='actualizar_unidadmedida'),
    path('unidadmedida/eliminar/<int:id>/', eliminar_unidadmedida, name='eliminar_unidadmedida'),
    
    #---> URL Conversion Unidad Medida
    path('conversionunidadmedida/', listar_conversionunidadmedida, name='listar_conversionunidadmedida'),
    path('conversionunidadmedida/crear/', crear_conversionunidadmedida, name='crear_conversionunidadmedida'),
    path('conversionunidadmedida/actualizar/<int:id>/', actualizar_conversionunidadmedida, name='actualizar_conversionunidadmedida'),
    path('conversionunidadmedida/eliminar/<int:id>/', eliminar_conversionunidadmedida, name='eliminar_conversionunidadmedida'),
    
    #---> URL Mercado
    path('mercado/', listar_mercados, name='listar_mercados'),
    path('mercado/crear/', crear_mercado, name='crear_mercado'),
    path('mercado/actualizar/<int:id>/', actualizar_mercado, name='actualizar_mercado'),
    path('mercado/eliminar/<int:id>/', eliminar_mercado, name='eliminar_mercado'),
    
    #---> URL Pais
    path('paises/', listar_paises, name='listar_paises'),
    path('paisesactivos/', listar_paises_activos, name='listar_paises_activos'),
    
    path('pais/crear/', crear_pais, name='crear_pais'),
    path('pais/actualizar/<int:id>/', actualizar_pais, name='actualizar_pais'),
    path('pais/eliminar/<int:id>/', eliminar_pais, name='eliminar_pais'),
    
    #---> URL Departamento
    path('departamento/', listar_departamentos, name='listar_departamentos'),
    path('departamentosactivos/', listar_departamentos_activos, name='listar_departamentos_activos'),
    path('departamento/crear/', crear_departamento, name='crear_departamento'),
    path('departamento/actualizar/<int:id>/', actualizar_departamento, name='actualizar_departamento'),
    path('departamento/eliminar/<int:id>/', eliminar_departamento, name='eliminar_departamento'),
    
    #---> URL Provincia
    path('provincia/', listar_provincias, name='listar_provincias'),
    path('provinciasactivas/', listar_provincias_activos, name='listar_provincias_activos'),
    path('provincia/crear/', crear_provincia, name='crear_provincia'),
    path('provincia/actualizar/<int:id>/', actualizar_provincia, name='actualizar_provincia'),
    path('provincia/eliminar/<int:id>/', eliminar_provincia, name='eliminar_provincia'),
    
    #---> URL Distrito
    path('distrito/', listar_distritos, name='listar_distritos'),
    path('distritosactivos/', listar_distritos_activos, name='listar_distritos_activos'),
    path('distrito/crear/', crear_distrito, name='crear_distrito'),
    path('distrito/actualizar/<int:id>/', actualizar_distrito, name='actualizar_distrito'),
    path('distrito/eliminar/<int:id>/', eliminar_distrito, name='eliminar_distrito'),
    
    #---> URL LocalidadCaserio
    path('localidadcaserio/', listar_localidadcaserio, name='listar_localidadcaserio'),
    path('localidadcaserio/crear/', crear_localidadcaserio, name='crear_localidadcaserio'),
    path('localidadcaserio/actualizar/<int:id>/', actualizar_localidadcaserio, name='actualizar_localidadcaserio'),
    path('localidadcaserio/eliminar/<int:id>/', eliminar_localidadcaserio, name='eliminar_localidadcaserio'),
    

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)