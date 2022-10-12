from Compilador import generador
from Compilador.Interfaces.nodo import Nodo


class Identificador(Nodo):
    def __init__(self,token,idnodo,id,linea,columna):
        super().__init__(token,idnodo)
        self.id = id
        self.linea = linea
        self.columna = columna


    def crearTabla(self,ts):
        pass


    def crearCodigo3d(self,ts):
        simbolo = ts.get(self.id,"variable")
        print(simbolo.direccionRel)

        tempPosId = generador.nuevoTemporal()
        self.expresion += tempPosId + " = P + "+str(simbolo.direccionRel) + ";\n"

        tempValId = generador.nuevoTemporal()
        self.expresion += tempValId + " = stack[(int)" + tempPosId + "];\n"
        self.ref = tempValId

        return self.expresion

    def calcTam(self):
        return 0