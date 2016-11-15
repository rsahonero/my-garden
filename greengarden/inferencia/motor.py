"""
El modulo motor contiene una clase con el mismo nombre la cual es capaz de
realizar un ciclo de inferencia empleando el algoritmo de encadenamiento
hacia adelante.
"""
from enum import Enum, unique

from ..models import Regla


@unique
class TipoDeEncadenamiento(Enum):
    hacia_atras = 0
    hacia_adelante = 1


class Motor:
    """Motor de Inferencia"""

    def __init__(self):
        self.memoria_trabajo = Memoria()
        self.hechos_marcados = []
        self.objetivo_en_curso = None
        self.objetivo_inicial = None
        self.objetivos_previos = None
        self.reglas_activas = Regla.objects.all()
        self.reglas_inactivas = []

    def asignar_valores_conocidos(self, valores_conocidos):
        """
        Etapa 1.1: Asigna a los objetos sus valores conocidos
        :param hechos_conocidos:
        """
        for k, v in valores_conocidos.items():
            self.memoria_trabajo.agregar_hecho(k.titulo, v)
            self.hechos_marcados.append(k)

    def cargar_objetivo_en_curso(self, hecho):
        """
        Etapa 1.2: Carga el objetivo en curso
        :param hecho: El nuevo objetivo en curso
        """
        self.objetivo_en_curso = hecho

    def verificar_objetivo(self):
        """
        Etapa 1.3: Verifica si el objetivo esta marcado
        :return: True si el objetivo en curso esta marcado
        """
        return self.objetivo_en_curso in self.hechos_marcados

    def cargar_objetivos(self):
        """
        Etapa 1.4 (si 1.3 es Falso):
            Designar como objetivo inicial el objetivo en curso
            Marcar el objetivo en curso
            Objetivos previos []
            Designar todas las reglas como activas
        """
        self.objetivo_inicial = self.objetivo_en_curso
        self.hechos_marcados.append(self.objetivo_en_curso)
        self.objetivos_previos = []
        self.buscar_regla()

    def buscar_regla(self):
        """
        Etapa 2: Busca una regla activa que incluya el objetivo en curso y
        ninguno de los objetos en objetivos previos, si se encuentra ir a la
        Etapa 3, caso contrario ir a la Etapa 5.
        """
        respuesta = None
        for regla in self.reglas_activas:
            conclusion = regla.conclusion
            hechos = regla.hecho_set.all()
            regla_valida = regla not in self.reglas_inactivas
            conclusion_valida = conclusion not in self.objetivos_previos
            hechos_validos = self.verificar_hechos(hechos)
            if (regla_valida and conclusion_valida and hechos_validos and
                    conclusion == self.objetivo_en_curso):
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
            if hecho in self.objetivos_previos:
                return False
        return True

    def ejecutar_regla(
            self,
            regla,
            tc=TipoDeEncadenamiento.hacia_atras):
        """
        Etapa 3: Ejecuta la regla relacionada al objetivo en curso, si concluye
        se asigna el valor obtenido al objetivo en curso, e ir a la Etapa 6,
        caso contrario ir a la Etapa 4
        :param regla: la regla a ser ejecutada
        :param tc: tipo de encadenamiento
        """
        valor = True
        for hecho in regla.hecho_set.all():
            hecho_valor = self.memoria_trabajo.obtener_valor(hecho.titulo)
            if hecho_valor is False:
                self.memoria_trabajo.agregar_hecho(regla.conclusion.titulo, False)
                valor = False
                return
            if hecho_valor is not None:
                valor &= hecho_valor
            else:
                if tc == TipoDeEncadenamiento.hacia_atras:
                    self.verificar_regla(regla)
                    return
                elif tc == TipoDeEncadenamiento.hacia_adelante:
                    return False
        if tc == TipoDeEncadenamiento.hacia_atras:
            self.memoria_trabajo.agregar_hecho(self.objetivo_en_curso.titulo, valor)
            self.validar_objetivo_en_curso()
        elif tc == TipoDeEncadenamiento.hacia_adelante:
            self.memoria_trabajo.agregar_hecho(regla.conclusion.titulo, valor)
            self.hechos_marcados.append(regla.conclusion)
            return True

    def verificar_regla(self, regla):
        """
        Etapa 4: Si todos los objetos de la regla estan marcados, se declara la
         regla como inactiva y se va a la Etapa 2
        """
        if (regla.conclusion in self.hechos_marcados and
                self.verificar_hechos_marcados(regla.hecho_set.all())):
            self.reglas_inactivas.append(regla)
            self.buscar_regla()
        else:
            self.objetivos_previos.append(self.objetivo_en_curso)
            for hecho in regla.hecho_set.all():
                hecho_valor = self.memoria_trabajo.obtener_valor(hecho.titulo)
                if hecho_valor is None:
                    self.objetivo_en_curso = hecho
                    self.hechos_marcados.append(hecho)
                    self.buscar_regla()
                    break

    def verificar_hechos_marcados(self, hechos):
        """
        Etapa 4.1: Verifica que los hechos esten marcados
        """
        resultado = True
        for hecho in hechos:
            hecho_valor = self.memoria_trabajo.obtener_valor(hecho.titulo)
            # Si el hecho es falso, la regla se deberia desactivar
            if hecho_valor is False:
                resultado = True
                break
            if hecho_valor in self.hechos_marcados:
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
        if self.objetivo_en_curso == self.objetivo_inicial:
            return True
        else:
            raise Exception('El valor es desconocido')

    def validar_objetivo_en_curso(self):
        """
        Etapa 6: Si el objetivo en curso es el mismo que el objetivo inicial ir
        a la Etapa 7, en otro caso designar el objetivo previo como objetivo en
        curso, eliminarlo de objetivos e ir a la Etapa 2
        """
        if self.objetivo_en_curso == self.objetivo_inicial:
            return True
        else:
            self.objetivo_en_curso = self.objetivos_previos[-1]
            del self.objetivos_previos[-1]
            self.buscar_regla()

    def obtener_objetivo_en_curso(self):
        """
        Etapa 7
        :return: True si el objetivo en curso tiene un valor
        """
        valor = self.memoria_trabajo.obtener_valor(self.objetivo_en_curso.titulo)
        if valor is not None:
            return self.objetivo_en_curso
        else:
            return None

    def encadenar_reglas(self):
        """
        Realiza un encadenamiento hacia adelante
        """
        for regla in self.reglas_activas:
            if regla not in self.reglas_inactivas:
                activada = self.ejecutar_regla(regla, TipoDeEncadenamiento.hacia_adelante)
                if activada:
                    self.reglas_inactivas.append(regla)
                    self.encadenar_reglas()
                else:
                    continue


class Memoria():
    """Memoria de Trabajo"""

    def __init__(self):
        self.hechos_conocidos = {}

    def obtener_valor(self, k):
        """Obtiene el valor del hecho conocido
        :param k: el titulo del Hecho
        """
        if k in self.hechos_conocidos:
            return self.hechos_conocidos[k]
        else:
            return None

    def agregar_hecho(self, k, v):
        """Agrega un hecho conocido a la memoria
        :param k: el titulo del hecho
        :param v: el valor del hecho
        """
        if k not in self.hechos_conocidos:
            self.hechos_conocidos[k] = v
