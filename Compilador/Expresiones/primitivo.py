from Compilador.Interfaces.nodo import Nodo
from Compilador.TablaSimbolo.tipo import tipo


class Primitivo(Nodo):
    def __init__(self,token,idNodo,valor):
        super().__init__(token,idNodo)
        self.ref = valor
        self.nombre = valor
        self.expresion = ""
        if self.tipo == "ENTERO":
            self.tipo = tipo.I64
        elif self.tipo == "DECIMAL":
            self.tipo = tipo.F64
        elif self.tipo == "CARACTER":
            self.tipo = tipo.CHAR
        elif self.tipo == "BOOLEAN":
            self.tipo = tipo.BOOL
        print("///",self.tipo)


    def crearCodigo3d(self,ts):
        self.expresion = ""
        self.ref = self.nombre
        return self.expresion

    def crearTabla(self,ts):
        pass

    def calcTam(self):
        return 1