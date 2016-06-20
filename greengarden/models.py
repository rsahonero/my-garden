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
    conclusion = models.ForeignKey('Hecho', default=None)

class Hecho(models.Model):
    """ Representa las premisas de una regla.

    :param valor: cadena de caracteres que representa el valor de la premisa.
    :param reglas: campo que representa la relacion de muchos a muchos con las
                   reglas.
    """
    valor = models.CharField(max_length=150)
    reglas = models.ManyToManyField(Regla)
