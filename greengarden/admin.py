from django.contrib import admin

from .models import Hecho, Regla, Detalle

class ReglaAdmin(admin.ModelAdmin):
    model = Regla


class HechoAdmin(admin.ModelAdmin):
    model = Hecho

class DetalleAdmin(admin.ModelAdmin):
    model = Detalle

admin.site.register(Hecho)
admin.site.register(Regla)
admin.site.register(Detalle)
