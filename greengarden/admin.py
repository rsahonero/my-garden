from django.contrib import admin
from django import forms

from tinymce.widgets import TinyMCE

from .models import (
    Hecho,
    Regla,
    Detalle,
    CondicionAtmosferica,
    ParametrosAtmosfericos,
    Estado)


class DetalleForm(forms.ModelForm):
    descripcion = forms.CharField(
                    widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))
    tratamiento = forms.CharField(
                    widget=TinyMCE(attrs={'cols': 80, 'rows': 10}),
                    required=False)

    class Meta:
        model = Detalle
        fields = ['hecho', 'imagen', 'descripcion', 'tratamiento']


class DetalleAdmin(admin.ModelAdmin):
    form = DetalleForm


class HechoReglasInline(admin.TabularInline):
    model = Hecho.reglas.through  # @UndefinedVariable


class ReglaAdmin(admin.ModelAdmin):
    list_filter = ('titulo',)
    inlines = [
        HechoReglasInline,
    ]


class HechoAdmin(admin.ModelAdmin):
    list_filter = ('titulo',)
    inlines = [
        HechoReglasInline,
    ]
    exclude = ('reglas',)

admin.site.register(Hecho, HechoAdmin)
admin.site.register(Regla, ReglaAdmin)
admin.site.register(Detalle, DetalleAdmin)
admin.site.register(CondicionAtmosferica)
admin.site.register(ParametrosAtmosfericos)
admin.site.register(Estado)
