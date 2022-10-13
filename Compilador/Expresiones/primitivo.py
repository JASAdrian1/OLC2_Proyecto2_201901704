from Compilador.Interfaces.nodo import Nodo
from Compilador.TablaSimbolo.tipo import tipo, Tipo


class Primitivo(Nodo):
    def __init__(self,token,idNodo,valor,tipo,fila,columna):
        super().__init__(token,idNodo)
        self.ref = valor
        self.nombre = valor
        self.valor = valor
        self.expresion = ""
        self.tipo = Tipo(tipo)
        print("///",self.tipo)


    def crearCodigo3d(self,ts):
        self.expresion = ""
        self.ref = self.nombre
        return self.expresion

    def crearTabla(self,ts):
        pass

    def calcTam(self):
        return 1