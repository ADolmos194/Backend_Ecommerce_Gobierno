from django.contrib import admin

from app_categorias.models import *

admin.site.register([Producto, TipoProducto])