from django.shortcuts import render
from django.utils import timezone

from .models import Hecho


def index(request):
    context = {
        'ultimo_escaneo': timezone.now()
    }
    return render(request, "greengarden/index.html", context)

def cuestionario(request):
    hechos_hojas = Hecho.objects.filter(categoria='H')
    hechos_flores = Hecho.objects.filter(categoria='F')
    hechos_tallo = Hecho.objects.filter(categoria='T')
    hechos_raiz = Hecho.objects.filter(categoria='R')
    context = {
        'hechos_hojas': hechos_hojas,
        'hechos_flores': hechos_flores,
        'hechos_tallo': hechos_tallo,
        'hechos_raiz': hechos_raiz
    }
    return render(request, "greengarden/cuestionario.html", context)
