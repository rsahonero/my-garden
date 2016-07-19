from django.contrib import admin

from .models import Hecho, Regla, Detalle, CondicionAtmosferica

class HechoReglasInline(admin.TabularInline):
    model = Hecho.reglas.through

class ReglaAdmin(admin.ModelAdmin):
    inlines = [
        HechoReglasInline,
    ]

class HechoAdmin(admin.ModelAdmin):
    inlines = [
        HechoReglasInline,
    ]
    exclude = ('reglas',)

admin.site.register(Hecho, HechoAdmin)
admin.site.register(Regla, ReglaAdmin)
admin.site.register(Detalle)
admin.site.register(CondicionAtmosferica)
