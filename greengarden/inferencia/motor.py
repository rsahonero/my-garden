"""
El modulo motor contiene una clase con el mismo nombre la cual es capaz de
realizar un ciclo de inferencia empleando el algoritmo de encadenamiento
hacia adelante.
"""
from ..models import Regla


class Motor():
    """
    El motor de inferencia emplea el algoritmo de encadenamiento hacia adelante
    para hallar una conclusion o meta.
    """
    def __init__(self, memoria_trabajo):
        """
        Crea una instancia del motor de inferencia

        :param _reglas_activadas: lista de reglas que fueron activadas.
        """
        self._reglas_activadas = []
        self._memoria_trabajo = memoria_trabajo

    def inferir(self):
        """
        La inferencia es un proceso recursivo que examina regla por regla hasta
        hallar una meta o hasta que se agoten las reglas.

        :return True: cuando un estado meta es alcanzado.
        :return False: cuando no se ha podido inferir un resultado.
        """
        for regla in Regla.objects.all():
            if self.regla_esta_activada(regla) is False:
                if self.emparejar_regla(regla):
                    self._reglas_activadas.append(regla)
                    self.agregar_conclusion(regla.conclusion)
                    if regla.conclusion.es_meta:
                        return True
                    else:
                        return self.inferir()
        return False

    def regla_esta_activada(self, regla):
        """
        Determina si una regla esta activada examinando la lista de reglas
        activadas.

        :param regla: la regla que sera examinada.
        :return True: si la regla esta activada.
        :return False: si la regla no fue activada.
        """
        for regla_activada in self._reglas_activadas:
            if regla_activada.titulo == regla.titulo:
                return True
        return False

    def emparejar_regla(self, regla):
        """
        Examina las premisas de la regla y determina si la misma debe activarse

        :param regla: regla cuyas premisas seran evaluadas.
        :return True: si las premisas emparejan con la memoria de trabajo.
        :return False: si alguna de las premisas no empareja con la memoria de
                        trabajo.
        """
        for premisa in regla.hecho_set.all():
            if self.emparejar_premisa(premisa) is False:
                return False
        return True

    def emparejar_premisa(self, premisa):
        """
        Evalua si la premisa esta presente en la memoria de trabajo.

        :param premisa: la premisa a ser evaluada.
        :return True: si la premisa esta en la memoria de trabajo.
        :return False: si la premisa no fue hallada en la memoria de trabajo.
        """
        for hecho in self._memoria_trabajo.obtener_hechos():
            if premisa.valor == hecho.valor:
                return True
        return False

    def agregar_conclusion(self, conclusion):
        """
        Inerta una conclusion en la memoria de trabajo.

        :param conclusion: la conclusion a ser agregada.
        """
        self._memoria_trabajo.insertar_hecho(conclusion)
