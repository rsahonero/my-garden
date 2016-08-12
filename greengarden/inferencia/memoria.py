"""
Contiene una clase estatica cuyo fin es almacenar de forma temporal los hechos.
"""


class Memoria():
    def __init__(self):
        self._hechos = []

    def obtener_hechos(self):
        return self._hechos

    def insertar_hecho(self, hecho):
        if self.el_hecho_existe(hecho) is False:
            self._hechos.add(hecho)

    def el_hecho_existe(self, nuevo_hecho):
        for hecho in self._hechos:
            if hecho.titulo == nuevo_hecho.titulo:
                return True
        return False

    def reiniciar_hechos(self):
        self._hechos = []
