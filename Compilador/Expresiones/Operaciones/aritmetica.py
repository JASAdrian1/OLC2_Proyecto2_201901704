from Compilador.Interfaces.nodo import Nodo
from Compilador.generador import nuevoTemporal


class Aritmetica(Nodo):
    def __init__(self, token, idNodo, exp1, exp2, expu, signo):
        super().__init__(token,idNodo)
        self.exp1 = exp1
        self.exp2 = exp2
        self.expu = expu
        self.signo = signo

    def crearCodigo3d(self,ts):
        self.exp1.crearCodigo3d(ts)
        self.exp2.crearCodigo3d(ts)
        if len(self.exp1.expresion) >1:
            self.expresion += self.exp1.expresion
        if len(self.exp2.expresion) >1:
            self.expresion += self.exp2.expresion
        self.ref = nuevoTemporal()
        signo = " "+self.signo+" "  #variable creada unicamente para agregar espacios al signo
        if self.signo == "+" or self.signo == "-" or self.signo == "*" or self.signo == "/" or self.signo == "^":
            self.expresion += str(self.ref) + " = " + str(self.exp1.ref) + signo + str(self.exp2.ref) + ";\n"

        #print(self.expresion, end="")
        return self.expresion

    def crearTabla(self,ts):
        pass

