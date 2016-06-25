from django.contrib import admin

from .models import Hecho, Regla

class ReglaAdmin(admin.ModelAdmin):
    model = Regla


class HechoAdmin(admin.ModelAdmin):
    model = Hecho

admin.site.register(Hecho)
admin.site.register(Regla)
