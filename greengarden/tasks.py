from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from celery import shared_task

from .models import Hecho
from .inferencia import motor, memoria

logger = get_task_logger(__name__)
memoria_trabajo = memoria.Memoria()
motor_inferencia = motor.Motor(memoria_trabajo)

def actualizar_memoria(temperatura, humedad, mes):
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

@periodic_task(
    run_every=(crontab(minute='*/5')),
    name='task_monitorizar_condiciones_atmosfericas',
    ignore_result=False
)
def task_monitorizar_condiciones_atmosfericas():
    temperatura_actual = 26
    humedad_relativa = 67
    mes = 'Octubre'
    actualizar_memoria(temperatura_actual, humedad_relativa, mes)
    logger.info("Monitorizacion completada")

@shared_task
def task_inferir(parameter_list):
    respuesta = None
    print(parameter_list)
    for hecho_id in parameter_list:
        print(hecho_id)
        memoria_trabajo.insertar_hecho(Hecho.objects.get(id=hecho_id))
    if motor_inferencia.inferir():
        print('Inferencia completada...')
        respuesta = memoria_trabajo.obtener_hechos()[-1].id
        memoria_trabajo.reiniciar_hechos()
    return respuesta
