from django.db import models


class Hecho(models.Model):
    valor = models.CharField(max_length=150)
