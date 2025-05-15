from django.contrib import admin

from app_maquinarias.models import *

admin.site.register([TipoMaquinaria, Maquinaria, SubMaquinaria])