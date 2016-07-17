"""
Contiene una clase estatica cuyo fin es almacenar de forma temporal los hechos.
"""
class Memoria():
    def __init__(self):
        self._hechos_compartidos = []
        self._hechos = []

    def obtener_hechos(self):
        if len(self._hechos_compartidos) > 0:
            for hecho in self._hechos_compartidos:
                self.insertar_hecho(hecho)
            return self._hechos
        return self._hechos

    def insertar_hecho(self, hecho):
        if self.el_hecho_existe(hecho) is False:
            self._hechos.append(hecho)

    def el_hecho_existe(self, nuevo_hecho):
        for hecho in self._hechos:
            if hecho.valor == nuevo_hecho.valor:
                return True
        return False

    def insertar_hecho_compartido(self, hecho):
        self._hechos_compartidos.append(hecho)

    def reiniciar_hechos(self):
        self._hechos = []

    def reiniciar_hechos_compartidos(self):
        self._hechos_compartidos = []
