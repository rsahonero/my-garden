from celery.task.schedules import crontab  # @UnresolvedImport
from celery.decorators import periodic_task  # @UnresolvedImport
from celery.utils.log import get_task_logger

from .models import Hecho, CondicionAtmosferica, ParametrosAtmosfericos
from .inferencia.motor import Motor

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/5')),
    name='task_monitorizar_condiciones_atmosfericas',
    ignore_result=False
)
def task_monitorizar_condiciones_atmosfericas():
    global metas
    for hecho in Hecho.objects.all():
        if hecho.es_monitorizable or hecho.es_meta:
            hecho.valor = None
            hecho.save()
    parametros_atmosfericos = ParametrosAtmosfericos.objects.get(pk=1)
    temperatura = parametros_atmosfericos.temperatura
    humedad = parametros_atmosfericos.humedad_relativa
    mes = parametros_atmosfericos.mes
    hecho_temperatura = None
    hecho_humedad = None

    if temperatura <= 15:
        hecho_temperatura = Hecho.objects.filter(titulo='temperatura baja')[0]
    if temperatura > 15 and temperatura < 26:
        hecho_temperatura = Hecho.objects.filter(titulo='temperatura media')[0]
    if temperatura > 25:
        hecho_temperatura = Hecho.objects.filter(titulo='temperatura alta')[0]

    if humedad >= 0 and humedad < 34:
        hecho_humedad = Hecho.objects.filter(titulo='humedad baja')[0]
    if humedad >= 34 and humedad < 67:
        hecho_humedad = Hecho.objects.filter(titulo='humedad media')[0]
    if humedad > 66 and humedad <= 100:
        hecho_humedad = Hecho.objects.filter(titulo='humedad alta')[0]

    hecho_mes = Hecho.objects.filter(titulo=mes.lower())[0]

    hechos_conocidos = {
        hecho_temperatura: True,
        hecho_humedad: True,
        hecho_mes: True,
    }

    motor_inferencia = Motor()
    motor_inferencia.asignar_valores_conocidos(hechos_conocidos)
    motor_inferencia.encadenar_reglas()
    metas = []
    for hecho in motor_inferencia.hechos_marcados:
        if hecho.titulo.startswith('probabilidad'):
            metas.append(str(hecho.id))

    condiciones_atmosfericas = CondicionAtmosferica.objects.get(pk=1)
    condiciones_atmosfericas.temperatura = hecho_temperatura.id
    condiciones_atmosfericas.humedad = hecho_humedad.id
    condiciones_atmosfericas.estacion = hecho_mes.id
    condiciones_atmosfericas.metas = ';'.join(metas)
    condiciones_atmosfericas.save()

    logger.info(motor_inferencia.hechos_marcados)
    logger.info("Monitorizacion completada")
    return True
