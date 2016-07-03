"""
Modelos de la aplicacion Green Garden.
"""
from django.db import models


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
    titulo = models.CharField(max_length=150, default=None)
    es_meta = models.BooleanField(default=False)
    reglas = models.ManyToManyField(Regla, blank=True)

    def __str__(self):
        return self.valor
