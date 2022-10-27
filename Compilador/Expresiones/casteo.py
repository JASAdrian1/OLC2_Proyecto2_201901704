from Compilador.Interfaces.nodo import Nodo
from Compilador.TablaSimbolo.tipo import Tipo


class Casteo(Nodo):
    def __init__(self,token,idnodo,valor,tipo,linea,columna):
        super().__init__(token,idnodo)
        self.valor = valor
        self.tipo = tipo
        self.linea = linea
        self.columna = columna


    def crearTabla(self,ts):
        pass

    def crearCodigo3d(self,ts):
        self.valor.crearCodigo3d(ts)
        self.valor.tipo = self.tipo
        self.ref = self.valor.ref
        self.expresion += self.valor.expresion
        return self.expresion


    def calcTam(self):
        return 0

