from Compilador.Interfaces.nodo import Nodo
from Compilador.TablaSimbolo.tipo import tipo


class Primitivo(Nodo):
    def __init__(self,token,idNodo):
        super().__init__(token,idNodo)
        print(self.tipo)
        if self.tipo == 'ENTERO':
            self.tipo = tipo.I64
            self.nombre = self.valor


    def crearCodigo3d(self,ts):
        self.expresion = ""
        self.ref = self.nombre

    def crearTabla(self,ts):
        pass