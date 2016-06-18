from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import Hecho


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
        self.assertTrue(type(hecho.valor) is str)

    def test_valor_no_supera_los_ciento_cincuenta_caracteres(self):
        """
        La longitud maxima de caracteres no debe ser mayor a 150
        """
        hecho = Hecho.objects.get(pk=1)
        hecho.valor = 'asd' * 55;
        with self.assertRaises(ValidationError):
            hecho.clean_fields()
