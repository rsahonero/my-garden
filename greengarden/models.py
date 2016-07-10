"""
Modelos de la aplicacion Green Garden.
"""
from django.db import models


CATEGORIAS = {
    ('N', 'Ninguno'),
    ('H', 'Hoja'),
    ('F', 'Flor'),
    ('T', 'Tallo'),
    ('R', 'Raiz'),
}

class Regla(models.Model):
    """ La clase regla forma parte de la base de conocimiento.

    :param titulo: nombre de la regla.
    :param conclusion: referencia a un hecho que sera agregado a la memoria de
                       trabajo.
    """
    titulo = models.CharField(max_length=150)
    conclusion = models.ForeignKey('Hecho', default=None, null=True, blank=True)

    def __str__(self):
        return self.titulo

class Hecho(models.Model):
    """ Representa las premisas de una regla.

    :param valor: cadena de caracteres que representa el valor de la premisa.
    :param titulo: el valor mostrado al usuario
    :param es_meta: True si el hecho es meta False de otra manera
    :param reglas: campo que representa la relacion de muchos a muchos con las
                   reglas.
    """
    valor = models.CharField(max_length=150)
    titulo = models.CharField(max_length=150, default='', blank=True)
    es_meta = models.BooleanField(default=False)
    categoria = models.CharField(max_length=1, default='N', choices=CATEGORIAS)
    reglas = models.ManyToManyField(Regla, blank=True)

    def __str__(self):
        return self.valor

class Detalle(models.Model):
    hecho = models.OneToOneField(
        Hecho,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    imagen = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=250)
    tratamiento = models.CharField(max_length=250)

    def __str__(self):
        return self.hecho.valor
