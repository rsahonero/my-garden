from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from .models import Hecho
from .inferencia.motor import Motor

motor_inferencia = Motor()
metas = Hecho.objects.filter(es_meta=True)
indice = 0


def index(request):
    global indice
    indice = 0
    context = {
        'temperatura': 'Alta',
        'humedad': 'Relativa',
        'estacion': 'Primavera',
        'ultimo_escaneo': timezone.now()
    }
    return render(request, "greengarden/index.html", context)


def cuestionario(request):
    memoria = []
    hecho = motor_inferencia._objetivo_en_curso
    hecho_contexto = Hecho.objects.filter(titulo=hecho.titulo)[0]
    for hecho_marcado in motor_inferencia._hechos_marcados:
        if hecho_marcado.valor is not None and hecho_marcado.es_meta is False:
            memoria.append(hecho_marcado)
    contexto = {
        'hecho': hecho_contexto,
        'memoria': memoria,
    }
    return render(request, "greengarden/cuestionario.html", contexto)


def inferir(request):
    global indice
    global metas
    if request.method == 'POST':
        for hecho in Hecho.objects.all():
            if hecho.es_monitorizable is False or hecho.es_meta:
                hecho.valor = None
                hecho.save()
                hechos_conocidos = {}
        motor_inferencia._hechos_marcados = []
        motor_inferencia.asignar_valores_conocidos(hechos_conocidos)
        motor_inferencia.cargar_objetivo_en_curso(metas[indice])

        try:
            if motor_inferencia.verificar_objetivo():
                print('El objetivo esta marcado')
            else:
                motor_inferencia.cargar_objetivos()
        except Exception:
            return HttpResponseRedirect(reverse('greengarden:cuestionario'))
        return HttpResponseRedirect(reverse('greengarden:conclusion'))
    return HttpResponseRedirect(reverse('greengarden:index'))


def evaluar(request):
    hecho = motor_inferencia._objetivo_en_curso
    if request.method == "POST":
        valor = request.POST["valor"]
        if valor == "Si":
            hecho.valor = True
        else:
            hecho.valor = False
        hecho.save()
    try:
        motor_inferencia.validar_objetivo_en_curso()
    except Exception:
        return HttpResponseRedirect(reverse('greengarden:cuestionario'))
    return HttpResponseRedirect(reverse('greengarden:conclusion'))


def conclusion(request):
    global indice
    hecho = motor_inferencia.obtener_objetivo_en_curso()
    hecho_contexto = Hecho.objects.filter(titulo=hecho.titulo)[0]
    if hecho.valor is not None:
        if hecho.valor:
            contexto = {
                'hecho': hecho_contexto
            }
            return render(
                    request,
                    "greengarden/conclusion.html",
                    context=contexto)
        else:
            if len(metas) - 1 > indice:
                indice = indice + 1
                motor_inferencia.cargar_objetivo_en_curso(metas[indice])
                try:
                    motor_inferencia.cargar_objetivos()
                except Exception:
                    return HttpResponseRedirect(
                            reverse('greengarden:cuestionario'))
            return render(request, "greengarden/index.html")


def actualizar(request):
    if request.method == 'GET':
        return JsonResponse({
            'tiempo_actual': str(timezone.now())
        })
