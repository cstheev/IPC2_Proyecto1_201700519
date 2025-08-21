# modelo.py
class EstacionBase:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

class SensorSuelo:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.frecuencias = {}  # idEstacion: frecuencia

class SensorCultivo:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.frecuencias = {}

class CampoAgricola:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.estaciones = Lista()
        self.sensores_suelo = Lista()
        self.sensores_cultivo = Lista()
