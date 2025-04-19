from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path('registros/', include('app_registros.urls')),
    path('categorias/', include('app_categorias.urls')),
    path('ofertas/', include('app_ofertas.urls')),
    path('demandas/', include('app_demandas.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)