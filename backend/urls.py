from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from backend.view import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('app/', include('app.urls')),
    path('autenticacion/', include('app_autenticacion.urls')),
    path('categorias/', include('app_categorias.urls')),
    path('appofertas/', include('app_ofertas.urls')),
    path('appdemandas/', include('app_demandas.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
