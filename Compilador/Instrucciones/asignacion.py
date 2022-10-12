from Compilador import generador
from Compilador.Interfaces.nodo import Nodo


class Asignacion(Nodo):
    def __init__(self,token,idnodo,id,valor,fila,columna):
        super().__init__(token,idnodo)
        self.id = id
        self.nuevoValor = valor
        self.fila = fila
        self.columna = columna

    def crearTabla(self,ts):
        pass

    def crearCodigo3d(self,ts):
        simbolo = ts.get(self.id, "variable")

        tempPosSimb = generador.nuevoTemporal()
        self.expresion += tempPosSimb + " = P + " + str(simbolo.direccionRel) + ";\n"

        self.nuevoValor.crearCodigo3d(ts)    #Se ejecuta el codigo 3d del nuevo valor que se le asignara a la varable
        self.expresion += self.nuevoValor.expresion     #Se concatena el codigo del nuevo valor al codigo que llevamos
        self.expresion += "stack[(int)"+tempPosSimb + "] = " + str(self.nuevoValor.ref) + ";\n"

        return self.expresion


    def calcTam(self):
        return 0