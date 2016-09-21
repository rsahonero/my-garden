"""
Modelos de la aplicacion Green Garden.
"""
from django.db import models

VALORES = {
    (None, ''),
    (True, 'Yes'),
    (False, 'No'),
}

ESTADOS = {
    ('AS', 'Controlado'),
    ('IN', 'Infectado'),
    ('RS', 'Riesgo')
}


class Regla(models.Model):
    """ La clase regla forma parte de la base de conocimiento.

    :param titulo: nombre de la regla.
    :param conclusion: referencia a un hecho que sera agregado a la memoria de
                       trabajo.
    """
    titulo = models.CharField(max_length=150)
    conclusion = models.ForeignKey(
                    'Hecho', default=None, null=True, blank=True)

    def __str__(self):
        return self.titulo


class Hecho(models.Model):
    """ Representa las premisas de una regla.

    :param valor: cadena de caracteres que representa el valor de la premisa.
    :param pregunta: la pregunta realizada al usuario para obtener el valor
    :param titulo: el valor mostrado al usuario
    :param es_meta: True si el hecho es meta False de otra manera
    :param es_monitorizable: True si el hecho se puede monitorear
    :param reglas: campo que representa la relacion de muchos a muchos con las
                   reglas.
    """
    valor = models.NullBooleanField(choices=VALORES, default=None, blank=True)
    titulo = models.CharField(max_length=150, default='', blank=True)
    es_meta = models.BooleanField(default=False)
    es_monitorizable = models.BooleanField(default=False)
    pregunta = models.CharField(max_length=200, blank=True)
    reglas = models.ManyToManyField(Regla, blank=True)

    def __str__(self):
        return self.titulo


class Detalle(models.Model):
    """ Representa el detalle de un hecho

    :param imagen: la direccion donde se encuentra la imagen
    :param descripcion: la descripcion de un hecho
    :param tratamiento: el tratamiento de un hecho
    """
    hecho = models.OneToOneField(
        Hecho,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    imagen = models.CharField(max_length=100)
    descripcion = models.TextField()
    tratamiento = models.TextField(blank=True)

    def __str__(self):
        return self.hecho.titulo


class CondicionAtmosferica(models.Model):
    """ Almacena los valores de las condiciones atmosfericas

    :param temperatura: la temperatura al momento de la monitorizacion
    :param humedad: la humedad al momento de la monitorizacion
    :param estacion: la estacion al momento de la monitorizacion
    :param metas: las metas encontradas al momento de la monitorizacion
    :param ultima_actualizacion: el momento en el que fue realizada la
                                 monitorizacion
    """
    temperatura = models.IntegerField()
    humedad = models.IntegerField()
    estacion = models.IntegerField()
    metas = models.CharField(max_length=50)
    ultima_actualizacion = models.DateTimeField(auto_now=True)


class ParametrosAtmosfericos(models.Model):
    """ Almacena los valores de los parametros atmosfericos

    :param temperatura: la temperatura obtenida de un servicio
    :param humedad_relativa: la humedad obtenida de un servicio
    :param mes: el mes obtenido de un servicio
    """
    temperatura = models.DecimalField(decimal_places=2, max_digits=4)
    humedad_relativa = models.DecimalField(decimal_places=2, max_digits=4)
    mes = models.CharField(max_length=50)


class Estado(models.Model):
    """ Almacena los valores de los estados de la monitorizacion

    :param titulo: el titulo del estado
    :param descripcion: la descripcion del estado
    :param imagen: la imagen asociada al estado
    :param codigo: el codigo del estado
    """
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.CharField(max_length=100)
    codigo = models.CharField(choices=ESTADOS, max_length=2)

    def __str__(self):
        return self.titulo
