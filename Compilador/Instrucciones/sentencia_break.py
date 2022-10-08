from Compilador.Interfaces.nodo import Nodo
from Compilador import generador


class Sentencia_Break(Nodo):
    def __init__(self, token, idnodo, fila, columna):
        super().__init__(token, idnodo)
        self.fila = fila
        self.columna = columna


    def crearTabla(self,ts):
        pass

    def crearCodigo3d(self,ts):
        return "break"
        pass
