from django.contrib import admin

from app.models import *

admin.site.register([Estado, UnidadMedida, ConversionUnidadMedida, Mercado, Pais, Departamento, Provincia, Distrito , CustomUser])
