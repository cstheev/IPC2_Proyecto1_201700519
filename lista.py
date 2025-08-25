from nodo import Nodo, NodoKV, NodoEntero

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

class ListaEnteros:
    def __init__(self):
        self.primero = None

    def agregar(self, valor):
        nuevo = NodoEntero(valor)
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
            yield actual.valor
            actual = actual.siguiente

    def es_igual(self, otra):
        a = self.primero
        b = otra.primero
        while a and b:
            if a.valor != b.valor:
                return False
            a = a.siguiente
            b = b.siguiente
        return a is None and b is None

class DiccionarioEnlazado:
    def __init__(self):
        self.primero = None

    def asignar(self, clave, valor):
        actual = self.primero
        while actual:
            if actual.clave == clave:
                actual.valor = valor
                return
            actual = actual.siguiente
        nuevo = NodoKV(clave, valor)
        nuevo.siguiente = self.primero
        self.primero = nuevo

    def obtener(self, clave):
        actual = self.primero
        while actual:
            if actual.clave == clave:
                return actual.valor
            actual = actual.siguiente
        return None

    def contiene(self, clave):
        actual = self.primero
        while actual:
            if actual.clave == clave:
                return True
            actual = actual.siguiente
        return False

    def recorrer(self):
        actual = self.primero
        while actual:
            yield actual.clave, actual.valor
            actual = actual.siguiente
