from celery.task.schedules import crontab  # @UnresolvedImport
from celery.decorators import periodic_task  # @UnresolvedImport
from celery.utils.log import get_task_logger
from celery import shared_task

from .models import Hecho, CondicionAtmosferica
from .inferencia import motor, memoria

logger = get_task_logger(__name__)
memoria_trabajo = memoria.Memoria()
motor_inferencia = motor.Motor(memoria_trabajo)


@periodic_task(
    run_every=(crontab(minute='*/2')),
    name='task_monitorizar_condiciones_atmosfericas',
    ignore_result=False
)
def task_monitorizar_condiciones_atmosfericas():
    temperatura = 26
    humedad = 67
    mes = 'Octubre'
    hecho_temperatura = None
    hecho_humedad = None

    if temperatura <= 15:
        hecho_temperatura = Hecho.objects.filter(valor='temperatura_baja')
    elif temperatura > 15 and temperatura <= 25:
        hecho_temperatura = Hecho.objects.filter(valor='temperatura_media')
    else:
        hecho_temperatura = Hecho.objects.filter(valor='temperatura_alta')

    if humedad <= 33:
        hecho_humedad = Hecho.objects.filter(valor='humedad_baja')
    elif humedad > 33 and humedad <= 66:
        hecho_humedad = Hecho.objects.filter(valor='humedad_media')
    else:
        hecho_humedad = Hecho.objects.filter(valor='humedad_alta')

    hecho_estacion = Hecho.objects.filter(valor=mes.lower())
    memoria_trabajo.insertar_hecho(hecho_estacion[0])
    motor_inferencia.inferir()

    condiciones_atmosfericas = CondicionAtmosferica.objects.get(pk=1)
    condiciones_atmosfericas.temperatura = hecho_temperatura[0].id
    condiciones_atmosfericas.humedad = hecho_humedad[0].id
    condiciones_atmosfericas.estacion = memoria_trabajo.obtener_hechos()[-1].id

    condiciones_atmosfericas.save()
    memoria_trabajo.reiniciar_hechos()
    motor_inferencia.reiniciar_reglas_activadas()

    logger.info("Monitorizacion completada")
    return True


@shared_task
def task_inferir(parameter_list):
    respuesta = None
    for hecho_id in parameter_list:
        memoria_trabajo.insertar_hecho(Hecho.objects.get(id=hecho_id))
    logger.info("Iniciando la inferencia...")
    if motor_inferencia.inferir():
        logger.info("Inferencia completada")
        respuesta = memoria_trabajo.obtener_hechos()[-1].id
        print(memoria_trabajo.obtener_hechos())
        memoria_trabajo.reiniciar_hechos()
        motor_inferencia.reiniciar_reglas_activadas()
    return respuesta
