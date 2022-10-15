from Compilador.Interfaces.nodo import Nodo
from Compilador.generador import nuevoTemporal


class Aritmetica(Nodo):
    def __init__(self, token, idNodo, exp1, exp2, expu, signo):
        super().__init__(token,idNodo)
        self.exp1 = exp1
        self.exp2 = exp2
        self.tipo = exp1.tipo
        print("Exp1 tipo: ",exp1.tipo)
        self.expu = expu
        self.signo = signo

    def crearCodigo3d(self,ts):
        if self.expu is False:
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

            #***ASIGNACION DE TIPO PROVISIONAL (FALTA QUE REALIZAR LA VALIDACION QUE LOS TIPOS DE LAS DOS EXPRESIONES COINCIDAN)
            self.tipo = self.exp1.tipo
            #print("tipo (expresion): ",self.tipo.tipo_string)
            #print(self.expresion, end="")
        else:
            self.exp1.crearCodigo3d(ts)
            if len(self.exp1.expresion) >1:
                self.expresion += self.exp1.expresion
            self.ref = nuevoTemporal()
            self.expresion += str(self.ref) + " = " + self.signo + str(self.exp1.ref) + ";\n"
            signo = " " + self.signo + " "  # variable creada unicamente para agregar espacios al signo
        return self.expresion

    def crearTabla(self,ts):
        self.exp1.crearTabla(ts)
        self.tipo = self.exp1.tipo


    def calcTam(self):
        return 0

