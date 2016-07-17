from django.test import TestCase

from ..inferencia import memoria, motor
from ..models import Hecho, Regla


class MemoriaTests(TestCase):
    def test_tiene_una_lista_de_hechos(self):
        """
        La memoria de trabajo deberia tener una lista de hechos
        """
        memoria_trabajo = memoria.Memoria()
        self.assertIsNotNone(memoria_trabajo.obtener_hechos())

    def test_se_puede_agregar_un_hecho(self):
        """
        Se deberia poder agregar hechos a la memoria de trabajo
        """
        hecho = Hecho()
        memoria_trabajo = memoria.Memoria()
        memoria_trabajo.insertar_hecho(hecho)
        self.assertTrue(len(memoria_trabajo.obtener_hechos()) > 0)

class MotorTests(TestCase):
    def setUp(self):
        Hecho.objects.create(valor='A')
        Hecho.objects.create(valor='B')
        Hecho.objects.create(valor='C')
        Hecho.objects.create(valor='D')
        Hecho.objects.create(valor='E')
        Hecho.objects.create(valor='F')
        Hecho.objects.create(valor='G')
        Hecho.objects.create(valor='H', es_meta=True)
        Hecho.objects.create(valor='X')

        Regla.objects.create(titulo='r1', conclusion=Hecho.objects.get(pk=6))
        Regla.objects.create(titulo='r2', conclusion=Hecho.objects.get(pk=1))
        Regla.objects.create(titulo='r3', conclusion=Hecho.objects.get(pk=1))
        Regla.objects.create(titulo='r4', conclusion=Hecho.objects.get(pk=9))
        Regla.objects.create(titulo='r5', conclusion=Hecho.objects.get(pk=5))
        Regla.objects.create(titulo='r6', conclusion=Hecho.objects.get(pk=8))
        Regla.objects.create(titulo='r7', conclusion=Hecho.objects.get(pk=4))
        Regla.objects.create(titulo='r8', conclusion=Hecho.objects.get(pk=1))

        Hecho.objects.get(pk=1).reglas.add(Regla.objects.get(pk=6))
        Hecho.objects.get(pk=2).reglas.add(Regla.objects.get(pk=1))
        Hecho.objects.get(pk=2).reglas.add(Regla.objects.get(pk=4))
        Hecho.objects.get(pk=3).reglas.add(Regla.objects.get(pk=3))
        Hecho.objects.get(pk=3).reglas.add(Regla.objects.get(pk=7))
        Hecho.objects.get(pk=3).reglas.add(Regla.objects.get(pk=8))
        Hecho.objects.get(pk=4).reglas.add(Regla.objects.get(pk=1))
        Hecho.objects.get(pk=4).reglas.add(Regla.objects.get(pk=2))
        Hecho.objects.get(pk=4).reglas.add(Regla.objects.get(pk=5))
        Hecho.objects.get(pk=5).reglas.add(Regla.objects.get(pk=1))
        Hecho.objects.get(pk=6).reglas.add(Regla.objects.get(pk=3))
        Hecho.objects.get(pk=7).reglas.add(Regla.objects.get(pk=2))
        Hecho.objects.get(pk=9).reglas.add(Regla.objects.get(pk=6))
        Hecho.objects.get(pk=9).reglas.add(Regla.objects.get(pk=8))

    def test_examinar_regla_es_valida(self):
        memoria_trabajo = memoria.Memoria()
        memoria_trabajo.insertar_hecho(Hecho.objects.get(pk=2))
        memoria_trabajo.insertar_hecho(Hecho.objects.get(pk=3))
        motor_inferencia = motor.Motor(memoria_trabajo)
        regla = Regla.objects.get(pk=4)
        self.assertTrue(motor_inferencia.emparejar_regla(regla))

    def test_agregar_conclusion(self):
        memoria_trabajo = memoria.Memoria()
        memoria_trabajo.insertar_hecho(Hecho.objects.get(pk=2))
        memoria_trabajo.insertar_hecho(Hecho.objects.get(pk=3))
        regla = Regla.objects.get(pk=4)
        motor_inferencia = motor.Motor(memoria_trabajo)
        if motor_inferencia.emparejar_regla(regla):
            motor_inferencia.agregar_conclusion(regla.conclusion)
        self.assertEqual('X', memoria_trabajo.obtener_hechos()[-1].valor)
        del memoria_trabajo.obtener_hechos()[-1]

    def test_inferir_con_estado_meta(self):
        memoria_trabajo = memoria.Memoria()
        memoria_trabajo.insertar_hecho(Hecho.objects.get(pk=2))
        memoria_trabajo.insertar_hecho(Hecho.objects.get(pk=3))
        motor_inferencia = motor.Motor(memoria_trabajo)
        self.assertTrue(motor_inferencia.inferir())
        self.assertEqual('H', memoria_trabajo.obtener_hechos()[-1].valor)

