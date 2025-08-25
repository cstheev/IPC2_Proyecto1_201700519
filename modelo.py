from lista import Lista, DiccionarioEnlazado

class EstacionBase:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

class SensorSuelo:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.frecuencias = DiccionarioEnlazado()

class SensorCultivo:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.frecuencias = DiccionarioEnlazado()

class CampoAgricola:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.estaciones = Lista()
        self.sensores_suelo = Lista()
        self.sensores_cultivo = Lista()
        self._matrices = None  # se mantiene para compatibilidad
