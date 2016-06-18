from django.test import TestCase

from ..inferencia.memoria import Memoria
from ..models import Hecho


class MemoriaTests(TestCase):
    def test_tiene_una_lista_de_hechos(self):
        """
        La memoria de trabajo deberia tener una lista de hechos
        """
        hechos = Memoria.hechos
        self.assertIsNotNone(hechos)

    def test_se_puede_agregar_un_hecho(self):
        """
        Se deberia poder agregar hechos a la memoria de trabajo
        """
        hecho = Hecho()
        Memoria.hechos.append(hecho)
        self.assertTrue(len(Memoria.hechos) > 0)
