from Compilador import generador
from Compilador.Interfaces.nodo import Nodo
from Compilador.TablaSimbolo.tipo import tipo, Tipo
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
            tipoVar = self.exp1.tipo
            if len(self.exp1.expresion) >1:
                self.expresion += self.exp1.expresion
            if len(self.exp2.expresion) >1:
                self.expresion += self.exp2.expresion
            self.ref = nuevoTemporal()
            signo = " "+self.signo+" "  #variable creada unicamente para agregar espacios al signo
            print("TTTT ",self.tipo)
            print(self.exp1.tipo.tipo_enum)
            print(self.exp2.tipo.tipo_enum)
            if tipoVar.tipo_enum != tipo.STR and tipoVar.tipo_enum != tipo.STRING:
                if self.signo == "+" or self.signo == "-" or self.signo == "*" or self.signo == "/" or self.signo == "^":
                    self.expresion += str(self.ref) + " = " + str(self.exp1.ref) + signo + str(self.exp2.ref) + ";\n"
            else:
                tempPosExp1 = generador.nuevoTemporal()
                tempPosExp2 = generador.nuevoTemporal()

                etiSalida = [generador.nuevaEtiqueta()]
                etiInicio = [generador.nuevaEtiqueta()]

                self.expresion += tempPosExp1 + " = " + str(self.exp1.ref) + ";\n"
                self.expresion += tempPosExp2 + " = heap[(int)" + tempPosExp1 + "];\n"

                print("ssssss")
                print(self.exp1.ref)
                #simboloExp1 = ts.get(self.exp1.pos)
                self.expresion += generador.soltarEtiqueta(etiInicio)
                self.expresion += "if(" + tempPosExp2 + " == -1)" + generador.generarGoto(etiSalida[0])
                self.expresion += tempPosExp1 + " = " + tempPosExp1 + "+ 1;\n"
                self.expresion += tempPosExp2 + " = heap[(int)" + tempPosExp1 + "];\n"
                self.expresion += generador.generarGoto(etiInicio[0])

                self.expresion += generador.soltarEtiqueta(etiSalida)
                self.expresion += "heap[(int)" + tempPosExp1 + "] = " + str(self.exp2.ref) + ";\n"
                self.expresion += str(self.ref) + " = " + str(self.exp1.ref) + ";\n"


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

