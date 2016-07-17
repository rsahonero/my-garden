from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from celery.result import AsyncResult

from .tasks import task_inferir
from .models import Detalle, Hecho
from .inferencia import memoria, motor

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
    contexto = {
        'hechos_hojas': hechos_hojas,
        'hechos_flores': hechos_flores,
        'hechos_tallo': hechos_tallo,
        'hechos_raiz': hechos_raiz
    }
    return render(request, "greengarden/cuestionario.html", contexto)

def inferir(request):
    if request.method == 'POST':
        hechos_ids = request.POST.getlist('hechos')
        result = task_inferir.delay(hechos_ids)
        return HttpResponseRedirect(reverse('greengarden:conclusion', args=(result.task_id,)))
    return HttpResponseRedirect(reverse('greengarden:index'))

def conclusion(request, task_id):
    result = AsyncResult(task_id)
    result.wait(1, True, 0.5, True, True)
    if result.ready():
        if result.successful():
            detalle = Detalle.objects.get(pk=result.result)
            contexto = {
                'detalle': detalle
            }
            return render(request, "greengarden/conclusion.html", contexto)
        else:
            print("No result")
    else:
        print("The result is not ready")
