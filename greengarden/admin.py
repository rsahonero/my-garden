from django.contrib import admin

from .models import Hecho


class HechoAdmin(admin.ModelAdmin):
    model = Hecho

admin.site.register(Hecho)
