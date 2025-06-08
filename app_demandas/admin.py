from django.contrib import admin

from app_demandas.models import *

admin.site.register([Demandas, TiposDemandas])