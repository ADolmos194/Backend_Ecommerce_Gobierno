from django.contrib import admin

from app_ofertas.models import *

admin.site.register([
    OfertasServicioAgrario, 
    OfertasProductosLacteos,
    OfertasFrutas,
    OfertasInsumoTecnologico,
    OfertasCerealesLegumbres,
    OfertasTuberculosRaices,
    OfertasPastosForrajes
    ])
