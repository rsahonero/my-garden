from django.test import TestCase

from ..models import CondicionAtmosferica, Detalle, Hecho, Regla


class HechoTests(TestCase):
    def setUp(self):
        Hecho.objects.create(valor=None)

    def test_valor_es_nulo(self):
        """
        El valor de un hecho puede ser desconocido
        """
        hecho = Hecho.objects.get(pk=1)
        self.assertIsNone(hecho.valor)

    def test_valor_es_verdadero(self):
        """
        El valor de un hecho puede ser verdadero
        """
        hecho = Hecho.objects.get(pk=1)
        hecho.valor = True
        self.assertTrue(hecho.valor)

    def test_valor_es_falso(self):
        """
        El valor de un hecho puede ser falso
        """
        hecho = Hecho.objects.get(pk=1)
        hecho.valor = False
        self.assertFalse(hecho.valor)

    def test_titulo_es_vacio(self):
        """
        El titulo de un hecho puede ser vacio
        """
        hecho = Hecho.objects.get(pk=1)
        self.assertEqual(hecho.titulo, '')


class ReglaTests(TestCase):
    def setUp(self):
        Regla.objects.create(titulo='regla_1')

    def test_titulo_no_nulo(self):
        """
        La regla debe tener un titulo
        """
        regla = Regla.objects.get(pk=1)
        self.assertEqual(regla.titulo, 'regla_1')


class DetalleTests(TestCase):
    def setUp(self):
        Hecho.objects.create(titulo='hecho')
        Detalle.objects.create(
            hecho=Hecho.objects.get(pk=1),
            imagen='imagen.jpg',
            descripcion='test',
            tratamiento='')

    def test_hecho_no_nulo(self):
        """
        Los detalles deberian estar relacionados a un hecho
        """
        hecho = Detalle.objects.get(pk=1)
        self.assertIsNotNone(hecho)

    def test_imagen_no_nulo(self):
        """
        Los detalles deben tener una referencia a una imagen
        """
        detalle = Detalle.objects.get(pk=1)
        self.assertEqual(detalle.imagen, 'imagen.jpg')

    def test_descripcion_no_nulo(self):
        """
        Los detalles deben tener una descripcion
        """
        detalle = Detalle.objects.get(pk=1)
        self.assertEqual(detalle.descripcion, 'test')

    def test_tratamiento_es_vacio(self):
        """
        El valor del tratamiento puede ser vacio
        """
        detalle = Detalle.objects.get(pk=1)
        self.assertEqual(detalle.tratamiento, '')


class CondicionAtmosfericaTests(TestCase):
    def setUp(self):
        CondicionAtmosferica.objects.create(
            temperatura=1,
            humedad=2,
            estacion=3)

    def test_condiciones_atmosfericas(self):
        """
        Las condiciones atmosfericas deberan tener los valores de humedad,
        temperatura y estacion distintos de 0
        """
        condicion_atmosferica = CondicionAtmosferica.objects.get(pk=1)
        self.assertTrue(condicion_atmosferica.temperatura > 0)
        self.assertTrue(condicion_atmosferica.humedad > 0)
        self.assertTrue(condicion_atmosferica.estacion > 0)
