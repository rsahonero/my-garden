from django.test import TestCase

from greengarden.models import Hecho, Regla
from ..inferencia.motor import Motor


class MotorTests(TestCase):
    def setUp(self):
        Hecho.objects.create(titulo='A')
        Hecho.objects.create(titulo='B')
        Hecho.objects.create(titulo='C')
        Hecho.objects.create(titulo='D')
        Hecho.objects.create(titulo='E')
        Hecho.objects.create(titulo='F')
        Hecho.objects.create(titulo='G')
        Hecho.objects.create(titulo='H')
        Hecho.objects.create(titulo='I')
        Hecho.objects.create(titulo='J')
        Hecho.objects.create(titulo='K')
        Hecho.objects.create(titulo='L')
        Hecho.objects.create(titulo='M')

        Regla.objects.create(
            titulo='regla_1', conclusion=Hecho.objects.get(pk=3))
        Regla.objects.create(
            titulo='regla_2', conclusion=Hecho.objects.get(pk=7))
        Regla.objects.create(
            titulo='regla_3', conclusion=Hecho.objects.get(pk=10))
        Regla.objects.create(
            titulo='regla_4', conclusion=Hecho.objects.get(pk=11))
        Regla.objects.create(
            titulo='regla_5', conclusion=Hecho.objects.get(pk=12))
        Regla.objects.create(
            titulo='regla_6', conclusion=Hecho.objects.get(pk=13))

        Hecho.objects.get(pk=1).reglas.add(Regla.objects.get(pk=1))
        Hecho.objects.get(pk=2).reglas.add(Regla.objects.get(pk=1))
        Hecho.objects.get(pk=4).reglas.add(Regla.objects.get(pk=2))
        Hecho.objects.get(pk=5).reglas.add(Regla.objects.get(pk=2))
        Hecho.objects.get(pk=6).reglas.add(Regla.objects.get(pk=2))
        Hecho.objects.get(pk=8).reglas.add(Regla.objects.get(pk=3))
        Hecho.objects.get(pk=9).reglas.add(Regla.objects.get(pk=3))
        Hecho.objects.get(pk=3).reglas.add(Regla.objects.get(pk=4))
        Hecho.objects.get(pk=7).reglas.add(Regla.objects.get(pk=4))
        Hecho.objects.get(pk=7).reglas.add(Regla.objects.get(pk=5))
        Hecho.objects.get(pk=10).reglas.add(Regla.objects.get(pk=5))
        Hecho.objects.get(pk=11).reglas.add(Regla.objects.get(pk=6))
        Hecho.objects.get(pk=12).reglas.add(Regla.objects.get(pk=6))

    def test_asignar_valores_conocidos(self):
        hecho_d = Hecho.objects.filter(titulo='D')[0]
        hecho_e = Hecho.objects.filter(titulo='E')[0]
        hecho_f = Hecho.objects.filter(titulo='F')[0]
        hecho_l = Hecho.objects.filter(titulo='L')[0]
        hechos_conocidos = {
            hecho_d: True,
            hecho_e: True,
            hecho_f: True,
            hecho_l: True
        }
        motor_inferencia = Motor()
        motor_inferencia.asignar_valores_conocidos(hechos_conocidos)
        self.assertTrue(hecho_d)
        self.assertTrue(hecho_e)
        self.assertTrue(hecho_f)
        self.assertTrue(hecho_l)

    def test_cargar_objetivo_en_curso(self):
        motor_inferencia = Motor()
        meta = Hecho.objects.filter(titulo='M')[0]
        motor_inferencia.cargar_objetivo_en_curso(meta)
        self.assertEqual(motor_inferencia._objetivo_en_curso, meta)

    def test_verificar_objetivo(self):
        motor_inferencia = Motor()
        meta = Hecho.objects.filter(titulo='M')[0]
        motor_inferencia.cargar_objetivo_en_curso(meta)
        self.assertFalse(motor_inferencia.verificar_objetivo())

    def test_cargar_objetivos(self):
        motor_inferencia = Motor()
        motor_inferencia.cargar_objetivos()
        self.assertEqual(
            motor_inferencia._objetivo_inicial,
            motor_inferencia._objetivo_en_curso)
        self.assertEqual(
            len(motor_inferencia._reglas_activas),
            Regla.objects.count())
        self.assertEqual(len(motor_inferencia._objetivos_previos), 0)
        self.assertTrue(
            motor_inferencia._objetivo_en_curso in
            motor_inferencia._hechos_marcados)
