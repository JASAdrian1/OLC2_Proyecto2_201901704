from Compilador.Interfaces.nodo import Nodo
from Compilador import generador
from Compilador.TablaSimbolo.tipo import Tipo


class Condicion_Logica(Nodo):
    def __init__(self, token, idnodo, exp1, exp2, signo, ):
        super().__init__(token,idnodo)
        self.exp1 = exp1
        self.exp2 = exp2
        self.tipo = Tipo("BOOL")
        self.etiV = []
        self.etiF = []
        self.signo = signo

    def crearTabla(self,ts):
        pass

    def crearCodigo3d(self,ts):
        self.etiV = []
        self.etiF = []

        if self.exp2 is not None:
            self.exp1.crearCodigo3d(ts)
            self.exp2.crearCodigo3d(ts)
            if self.signo == "&&":
                self.expresion += self.exp1.expresion
                self.expresion += generador.soltarEtiqueta(self.exp1.etiV)
                self.expresion += self.exp2.expresion
                self.etiV = self.exp2.etiV
                self.etiF = generador.unirEtiquetas(self.exp1.etiF, self.exp2.etiF)
            elif self.signo == "||":
                self.expresion += self.exp1.expresion
                self.expresion += generador.soltarEtiqueta(self.exp1.etiF)
                self.expresion += self.exp2.expresion
                self.etiF = self.exp2.etiF
                self.etiV = generador.unirEtiquetas(self.exp1.etiV, self.exp2.etiV)
        else:
            if self.signo == "(":
                self.exp1.crearCodigo3d(ts)
                self.etiV = self.exp1.etiV
                self.etiF = self.exp1.etiF
            elif self.signo == "!":
                self.exp1.crearCodigo3d(ts)
                self.expresion += self.exp1.expresion
                self.etiV = self.exp1.etiF
                self.etiF = self.exp1.etiV
            else:
                self.etiV.append(generador.nuevaEtiqueta())
                self.etiF.append(generador.nuevaEtiqueta())
                if self.exp1 == "true":
                    self.expresion += generador.generarGoto(self.etiV[0])
                elif self.exp1 == "false":
                    #print("HAHAHAH")
                    self.expresion += generador.generarGoto(self.etiF[0])

        print(self.expresion)
        return self.expresion

    def calcTam(self):
        return 1