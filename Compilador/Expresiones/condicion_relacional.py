from Compilador import generador
from Compilador.Interfaces.nodo import Nodo
from Compilador.TablaSimbolo.tipo import tipo, Tipo


class Condicion_Relacional(Nodo):
    def __init__(self, token, idnodo, exp1, exp2, signo):
        super().__init__(token,idnodo)
        self.exp1 = exp1
        self.exp2 = exp2
        self.signo = signo
        self.tipo = Tipo("BOOL")
        self.etiV = []
        self.etiF = []

    def crearTabla(self,ts):
        pass

    def crearCodigo3d(self,ts):
        self.exp1.crearCodigo3d(ts)
        self.exp2.crearCodigo3d(ts)
        self.expresion += self.exp1.expresion
        self.expresion += self.exp2.expresion

        self.etiV = []
        self.etiF = []
        self.etiV.append(generador.nuevaEtiqueta())
        self.etiF.append(generador.nuevaEtiqueta())

        cadenaCondicion = str(self.exp1.ref) + " " + self.signo + " " + str(self.exp2.ref)
        self.expresion += "if (" + cadenaCondicion + ") goto " + self.etiV[0] + ";\n"
        self.expresion += generador.generarGoto(self.etiF[0])
        print(self.expresion)
        return self.expresion

    def calcTam(self):
        return 1