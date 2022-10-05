from Compilador.Interfaces.nodo import Nodo
from Compilador import generador


class Declaracion(Nodo):
    def __init__(self,token, idnodo, id, valor):
        super().__init__(token,idnodo)
        self.id = id
        self.valor = valor

    def crearTabla(self,ts):
        pass

    def crearCodigo3d(self,ts):
        pass