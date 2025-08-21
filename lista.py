# lista.py
from nodo import Nodo

class Lista:
    def __init__(self):
        self.primero = None

    def agregar(self, dato):
        nuevo = Nodo(dato)
        if not self.primero:
            self.primero = nuevo
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo

    def recorrer(self):
        actual = self.primero
        while actual:
            yield actual.dato
            actual = actual.siguiente
