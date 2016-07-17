"""
Contiene una clase estatica cuyo fin es almacenar de forma temporal los hechos.
"""
class Memoria():
    def __init__(self):
        self._hechos_compartidos = []
        self._conclusiones_monitoreo = []
        self._hechos = []

    def obtener_hechos(self):
        return self._hechos

    def insertar_hecho(self, hecho):
        self._hechos.append(hecho)

    def insertar_hecho_compartido(self):
        self._hechos_compartidos.append(hecho)

    def reiniciar_hechos(self):
        self._hechos = []

    def reiniciar_hechos_compartidos(self):
        self._hechos_compartidos = []
