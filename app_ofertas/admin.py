from django.contrib import admin

from app_ofertas.models import *

admin.site.register([OrfetaServicioAgrario, OrfetaProductosLacteos, OrfetasFrutas, OrfetaInsumoTecnologico, OrfetaCerealesLegumbres, OrfetaTuberculosRaices, OrfetaPastosForrajes])
