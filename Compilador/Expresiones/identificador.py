from Compilador import generador
from Compilador.Interfaces.nodo import Nodo
from Compilador.TablaSimbolo.tipo import Tipo


class Identificador(Nodo):
    def __init__(self,token,idnodo,id,linea,columna):
        super().__init__(token,idnodo)
        self.id = id
        self.linea = linea
        self.columna = columna


    def crearTabla(self,ts):
        simbolo = ts.get(self.id,"variable")
        self.tipo = Tipo(simbolo.tipo_dato.tipo_string)


    def crearCodigo3d(self,ts):
        simbolo = ts.get(self.id,"variable")
        self.tipo = Tipo(simbolo.tipo_dato.tipo_string)
        #print("/*",self.tipo.tipo_string)

        tempPosId = generador.nuevoTemporal()
        self.expresion += tempPosId + " = P + "+str(simbolo.direccionRel) + ";\n"

        tempValId = generador.nuevoTemporal()
        self.expresion += tempValId + " = stack[(int)" + tempPosId + "];\n"
        self.ref = tempValId

        return self.expresion


    def actualizarReferencia(self,simbolo):
        tempNewPos = generador.nuevoTemporal()
        self.expresion += tempNewPos + " = P + " + str(simbolo.direccionRel) + ";\n"
        self.expresion += self.ref + " = stack[(int)" + tempNewPos + "];\n"
        return self.expresion


    def calcTam(self):
        return 0