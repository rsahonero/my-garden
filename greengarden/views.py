from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from .models import Hecho, CondicionAtmosferica, Regla, Estado
from .inferencia.motor import Motor

indice = 0
motor_inferencia = Motor()
metas = []
hechos_conocidos = {}


def cargar_metas():
    metas = []
    condicion_atmosferica = CondicionAtmosferica.objects.get(pk=1)
    meta_ids = condicion_atmosferica.metas.split(';')
    for meta_id in meta_ids:
        hecho = Hecho.objects.get(pk=meta_id)
        hechos_conocidos[hecho] = True
        for regla in Regla.objects.filter(conclusion__es_meta=True):
            if hecho in regla.hecho_set.all():
                metas.append(regla.conclusion)
                break
    return metas


def home(request):
    return render(request, 'greengarden/home.html')


def ayuda(request):
    return render(request, "greengarden/ayuda.html")


def index(request, codigo=None):
    global indice
    global metas
    metas = []
    indice = 0
    estado = None
    condicion_atmosferica = CondicionAtmosferica.objects.get(pk=1)
    meta_ids = condicion_atmosferica.metas.split(';')
    if len(meta_ids) > 0 and codigo is None:
        estado = Estado.objects.filter(codigo='RS')[0]
    elif codigo is not None:
        estado = Estado.objects.filter(codigo='AS')[0]

    context = {
        'temperatura': Hecho.objects.get(pk=condicion_atmosferica.temperatura),
        'humedad': Hecho.objects.get(pk=condicion_atmosferica.humedad),
        'estacion': Hecho.objects.get(pk=condicion_atmosferica.estacion),
        'ultimo_escaneo': condicion_atmosferica.ultima_actualizacion,
        'estado': estado,
    }
    return render(request, "greengarden/index.html", context)


def cuestionario(request):
    hechos_conocidos = motor_inferencia.memoria_trabajo.hechos_conocidos
    memoria = {k:v for (k,v) in hechos_conocidos.items() if not k.startswith('probabilidad') }
    hecho = motor_inferencia.objetivo_en_curso
    hecho_contexto = Hecho.objects.filter(titulo=hecho.titulo)[0]
    contexto = {
        'hecho': hecho_contexto,
        'memoria': memoria,
    }
    return render(request, "greengarden/cuestionario.html", contexto)


def inferir(request):
    global indice
    global metas
    global hechos_conocidos
    metas = cargar_metas()
    if request.method == 'POST':
        motor_inferencia.hechos_marcados = []
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
    hecho = motor_inferencia.objetivo_en_curso
    if request.method == "POST":
        valor = request.POST["valor"]
        if valor == "Si":
            motor_inferencia.memoria_trabajo.agregar_hecho(hecho.titulo, True)
        else:
            motor_inferencia.memoria_trabajo.agregar_hecho(hecho.titulo, False)
    try:
        motor_inferencia.validar_objetivo_en_curso()
    except Exception:
        return HttpResponseRedirect(reverse('greengarden:cuestionario'))
    return HttpResponseRedirect(reverse('greengarden:conclusion'))


def conclusion(request):
    global indice
    hecho = motor_inferencia.obtener_objetivo_en_curso()
    hecho_contexto = Hecho.objects.filter(titulo=hecho.titulo)[0]
    hecho_valor = motor_inferencia.memoria_trabajo.obtener_valor(hecho.titulo)
    if hecho_valor is not None:
        if hecho_valor is True:
            motor_inferencia.memoria_trabajo.hechos_conocidos = {}
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
                    return HttpResponseRedirect(reverse('greengarden:cuestionario'))
            motor_inferencia.memoria_trabajo.hechos_conocidos = {}
            return HttpResponseRedirect(reverse('greengarden:index', args=[1]))


def actualizar(request):
    if request.method == 'GET':
        condicion_atmosferica = CondicionAtmosferica.objects.get(pk=1)
        estacion = Hecho.objects.get(pk=condicion_atmosferica.estacion)
        temperatura = Hecho.objects.get(pk=condicion_atmosferica.temperatura)
        humedad = Hecho.objects.get(pk=condicion_atmosferica.humedad)
        return JsonResponse({
            'tiempo_actual': condicion_atmosferica.ultima_actualizacion,
            'estacion': estacion.titulo.capitalize(),
            'temperatura': temperatura.titulo.capitalize(),
            'humedad': humedad.titulo.capitalize()
        })
