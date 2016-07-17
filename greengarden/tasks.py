from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from celery import shared_task

from .models import Hecho
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
    hecho_estacion = None

    if temperatura <= 15:
        hecho_temperatura = Hecho.objects.filter(valor='menor_15_grados')
    elif temperatura > 15 and temperatura <= 25:
        hecho_temperatura = Hecho.objects.filter(valor='entre_16_24_grados')
    else:
        hecho_temperatura = Hecho.objects.filter(valor='mayor_25_grados')

    if humedad <= 33:
        hecho_humedad = Hecho.objects.filter(valor='menor_33_porciento')
    elif humedad > 33 and humedad <= 66:
        hecho_humedad = Hecho.objects.filter(valor='entre_34_66_porciento')
    else:
        hecho_humedad = Hecho.objects.filter(valor='mayor_66_porciento')

    hecho_estacion = Hecho.objects.filter(valor=mes.lower())

    memoria_trabajo.reiniciar_hechos_compartidos()
    memoria_trabajo.insertar_hecho_compartido(hecho_temperatura[0])
    memoria_trabajo.insertar_hecho_compartido(hecho_humedad[0])
    memoria_trabajo.insertar_hecho_compartido(hecho_estacion[0])

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
