from django.contrib import admin

from app_anuncios.models import *

admin.site.register([TipoAnuncio, AnuncioCompraVenta, AnuncioTrabajo, AnuncioMaquinaria])