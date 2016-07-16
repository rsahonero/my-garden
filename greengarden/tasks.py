from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/5')),
    name='task_monitorizar_condiciones_atmosfericas',
    ignore_result=False
)
def task_monitorizar_condiciones_atmosfericas():
    print("Hello World")
    logger.info("Monitorizacion completada")