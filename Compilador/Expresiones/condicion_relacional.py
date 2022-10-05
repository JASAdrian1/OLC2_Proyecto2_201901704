from Compilador import generador
from Compilador.Interfaces.nodo import Nodo


class Condicion_Relacional(Nodo):
    def __init__(self, token, idnodo, exp1, exp2, signo):
        super().__init__(token,idnodo)
        self.exp1 = exp1
        self.exp2 = exp2
        self.signo = signo
        self.etiV = []
        self.etiF = []

    def crearTabla(self,ts):
        pass

    def crearCodigo3d(self,ts):
        self.etiV.append(generador.nuevaEtiqueta())
        self.etiF.append(generador.nuevaEtiqueta())
        cadenaCondicion = str(self.exp1.ref) + " " + self.signo + " " + str(self.exp2.ref)
        self.expresion += "if (" + cadenaCondicion + ") goto " + self.etiV[0] + "\n"
        self.expresion += "goto " + self.etiF[0] + "\n"
        print(self.expresion)
        return self.expresion