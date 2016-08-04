from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import Hecho, Regla


class HechoTests(TestCase):
    def setUp(self):
        Hecho.objects.create(valor='test')

    def test_valor_no_es_nulo(self):
        """
        El valor de un hecho no debe ser nulo
        """
        hecho = Hecho.objects.get(pk=1)
        self.assertIsNotNone(hecho.valor)

    def test_valor_es_texto(self):
        """
        El valor de un hecho debe ser una cadena de caracteres
        """
        hecho = Hecho.objects.get(pk=1)
        self.assertTrue(isinstance(hecho.valor, str))

    def test_valor_no_supera_los_ciento_cincuenta_caracteres(self):
        """
        La longitud maxima de caracteres no debe ser mayor a 150
        """
        hecho = Hecho.objects.get(pk=1)
        hecho.valor = 'asd' * 55
        with self.assertRaises(ValidationError):
            hecho.clean_fields()


class ReglaTests(TestCase):
    def setUp(self):
        Hecho.objects.create(valor='hecho1')
        Hecho.objects.create(valor='hecho2')
        Regla.objects.create(
            titulo='regla1',
            conclusion=Hecho.objects.get(pk=2)
        )

    def test_titulo_no_es_nulo(self):
        """
        El titulo de una regla no debe ser nulo
        """
        regla = Regla.objects.get(pk=1)
        self.assertIsNotNone(regla.titulo)

    def test_titulo_es_texto(self):
        """
        El titulo de una regla debe ser una cadena de caracteres
        """
        regla = Regla.objects.get(pk=1)
        self.assertTrue(isinstance(regla.titulo, str))

    def test_titulo_no_supera_los_ciento_cincuenta_caracteres(self):
        """
        El titulo de la regla no debe superar los 150 caracteres
        """
        regla = Regla.objects.get(pk=1)
        regla.titulo = 'asd' * 55
        with self.assertRaises(ValidationError):
            regla.clean_fields()

    def test_tiene_una_lista_de_echos(self):
        """
        Las reglas deberian tener una lista de hechos
        """
        regla = Regla.objects.get(pk=1)
        hecho = Hecho.objects.get(pk=1)
        hecho.reglas.add(regla)
        self.assertTrue(len(regla.hecho_set.all()) == 1)

    def test_tiene_una_conclusion(self):
        """
        Las reglas deberian tener solo una conclusion
        """
        regla = Regla.objects.get(pk=1)
        self.assertIsNotNone(regla.conclusion)
