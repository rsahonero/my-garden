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
    def __init__(self):
        """
        Crea una instancia del motor de inferencia
        """
        self._hechos_marcados = []
        self._objetivo_en_curso = None
        self._objetivo_inicial = None
        self._objetivos_previos = None
        self._reglas_activas = None
        self._reglas_inactivas = []

    def asignar_valores_conocidos(self, hechos_conocidos):
        """
        Etapa 1.1: Asigna a los objetos sus valores conocidos
        :param hechos_conocidos:
        """
        for k, v in hechos_conocidos.items():
            k.valor = v
            k.save()
            self._hechos_marcados.append(k)

    def cargar_objetivo_en_curso(self, hecho):
        """
        Etapa 1.2: Carga el objetivo en curso
        :param hecho: El nuevo objetivo en curso
        """
        self._objetivo_en_curso = hecho

    def verificar_objetivo(self):
        """
        Etapa 1.3: Verifica si el objetivo esta marcado
        :return: True si el objetivo en curso esta marcado
        """
        return self._objetivo_en_curso in self._hechos_marcados

    def cargar_objetivos(self):
        """
        Etapa 1.4 (si 1.3 es Falso):
            Designar como objetivo inicial el objetivo en curso
            Marcar el objetivo en curso
            Objetivos previos []
            Designar todas las reglas como activas
        """
        self._objetivo_inicial = self._objetivo_en_curso
        self._hechos_marcados.append(self._objetivo_en_curso)
        self._objetivos_previos = []
        self._reglas_activas = Regla.objects.all()
        self.buscar_regla()

    def buscar_regla(self):
        """
        Etapa 2: Busca una regla activa que incluya el objetivo en curso y
        ninguno de los objetos en objetivos previos, si se encuentra ir a la
        Etapa 3, caso contrario ir a la Etapa 5.
        """
        respuesta = None
        for regla in self._reglas_activas:
            conclusion = regla.conclusion
            hechos = regla.hecho_set.all()
            regla_valida = regla not in self._reglas_inactivas
            conclusion_valida = conclusion not in self._objetivos_previos
            hechos_validos = self.verificar_hechos(hechos)
            if (regla_valida and conclusion_valida and hechos_validos and
                    conclusion == self._objetivo_en_curso):
                respuesta = regla
                break
        if respuesta is not None:
            self.ejecutar_regla(respuesta)
        else:
            self.evaluar_objetivo_en_curso()

    def verificar_hechos(self, hechos):
        """
        Etapa 2.1: Verifica que los hechos no esten en los objetivos previos
        :param hechos:
        """
        for hecho in hechos:
            if hecho in self._objetivos_previos:
                return False
        return True

    def ejecutar_regla(self, regla):
        """
        Etapa 3: Ejecuta la regla relacionada al objetivo en curso, si concluye
        se asigna el valor obtenido al objetivo en curso, e ir a la Etapa 6,
        caso contrario ir a la Etapa 4
        :param regla: la regla a ser ejecutada
        """
        print('Entrando a la Etapa 3')
        valor = True
        for hecho in regla.hecho_set.all():
            if hecho.valor is not None:
                valor &= hecho.valor
            else:
                self.verificar_regla(regla)
                return
        self._objetivo_en_curso.valor = valor
        self._objetivo_en_curso.save()
        self.validar_objetivo_en_curso()

    def verificar_regla(self, regla):
        """
        Etapa 4: Si todos los objetos de la regla estan marcados, se declara la
         regla como inactiva y se va a la Etapa 2
        """
        if (regla.conclusion in self._hechos_marcados and
                self.verificar_hechos_marcados(regla.hecho_set.all())):
            self._reglas_inactivas.append(regla)
            self.buscar_regla()
        else:
            self._objetivos_previos.append(self._objetivo_en_curso)
            for hecho in regla.hecho_set.all():
                if hecho.valor is None:
                    self._objetivo_en_curso = hecho
                    self._hechos_marcados.append(hecho)
                    self.buscar_regla()
                    break

    def verificar_hechos_marcados(self, hechos):
        """
        Etapa 4.1: Verifica que los hechos esten marcados
        :param hechos:
        """
        resultado = True
        for hecho in hechos:
            if hecho in self._hechos_marcados:
                resultado &= True
            else:
                resultado &= False
                break
        return resultado

    def evaluar_objetivo_en_curso(self):
        """
        Etapa 5: Si el objetivo en curso es el mismo que el objetivo inicial se
        va a la 7, en otro caso, se pregunta al usuario por el valor del del
        objetivo en curso.Si el valor es proporcionado, es asignado y se pasa
        a la Etapa 6, caso contrario se pasa a la Etapa 6.
        """
        if self._objetivo_en_curso == self._objetivo_inicial:
            return True
        else:
            raise Exception('El valor es desconocido')

    def validar_objetivo_en_curso(self):
        """
        Etapa 6: Si el objetivo en curso es el mismo que el objetivo inicial ir
        a la Etapa 7, en otro caso designar el objetivo previo como objetivo en
        curso, eliminarlo de objetivos e ir a la Etapa 2
        """
        if self._objetivo_en_curso == self._objetivo_inicial:
            return True
        else:
            self._objetivo_en_curso = self._objetivos_previos[-1]
            del self._objetivos_previos[-1]
            self.buscar_regla()

    def obtener_objetivo_en_curso(self):
        """
        Etapa 7
        :return: True si el objetivo en curso tiene un valor
        """
        if self._objetivo_en_curso.valor is not None:
            return self._objetivo_en_curso
        else:
            return None
