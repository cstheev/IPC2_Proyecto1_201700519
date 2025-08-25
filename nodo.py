class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class NodoKV:
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.siguiente = None

class NodoEntero:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None
