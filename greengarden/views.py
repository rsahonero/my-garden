from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from .models import Hecho
from .inferencia import memoria, motor


motor_inferencia = motor.Motor()

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

def inferir(request):
    if request.method == 'POST':
        hechos_ids = request.POST.getlist('hechos')
        for hecho_id in hechos_ids:
            memoria.HECHOS.append(Hecho.objects.get(id=hecho_id))
        #motor_inferencia.inferir()
    return HttpResponseRedirect(reverse('greengarden:index'))
