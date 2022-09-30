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
        self.expresion += self.exp1.expresion + "\n"
        self.expresion += self.exp2.expresion + "\n"
        self.ref = nuevoTemporal()
        if self.signo == "+":
            self.expresion += str(self.ref) + " = " + str(self.exp1.ref) + " + " + str(self.exp2.ref)
        elif self.signo == "-":
            self.expresion += str(self.ref) + " = " + str(self.exp1.ref) + " - " + str(self.exp2.ref)
        elif self.signo == "/":
            self.expresion += str(self.ref) + " = " + str(self.exp1.ref) + " / " + str(self.exp2.ref)
        elif self.signo == "*":
            self.expresion += str(self.ref) + " = " + str(self.exp1.ref) + " * " + str(self.exp2.ref)
        elif self.signo == "^":
            self.expresion += str(self.ref) + " = " + str(self.exp1.ref) + " ^ " + str(self.exp2.ref)

        print(self.expresion)

    def crearTabla(self,ts):
        pass

