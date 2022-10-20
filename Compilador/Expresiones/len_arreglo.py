from Compilador import generador
from Compilador.Expresiones.acceso_arreglo import Acceso_Arreglo
from Compilador.Expresiones.identificador import Identificador
from Compilador.Interfaces.nodo import Nodo
from Compilador.TablaSimbolo.tipo import tipo


class Len_Arreglo(Nodo):
    def __init__(self,token,idnodo,arreglo,linea,columna):
        super().__init__(token,idnodo)
        self.arreglo = arreglo
        self.linea = linea
        self.columna = columna

    def crearTabla(self,ts):
        pass


    def crearCodigo3d(self,ts):
        simbolo = ts.get(self.arreglo.id)
        print(simbolo)
        print(simbolo.dimensiones)
        print(simbolo.tipo_dato.tipo_enum)
        #print(self.arreglo.accesoArreglo)

        tempLongitud = generador.nuevoTemporal()
        tempPosicionArr = generador.nuevoTemporal()
        tempPosArrHeap = generador.nuevoTemporal()

        if simbolo.tipo_dato.tipo_enum == tipo.ARRAY:
            if isinstance(self.arreglo,Identificador):
                self.expresion += tempPosicionArr + " = P + " + str(simbolo.direccionRel) + ";\n"
                self.expresion += tempPosArrHeap + " = stack[(int)" + tempPosicionArr + "];\n"
                self.expresion += tempLongitud + " = heap[(int)" + tempPosArrHeap + "];\n"
                self.ref = tempLongitud
            elif isinstance(self.arreglo,Acceso_Arreglo):
                self.expresion += tempPosicionArr + " = P + " + str(simbolo.direccionRel) + ";\n"
                self.expresion += tempPosArrHeap + " = stack[(int)" + tempPosicionArr + "];\n"
                self.expresion += tempPosArrHeap + " = " + tempPosArrHeap + " + " + str(len(self.arreglo.accesoArreglo)) + ";\n"
                self.expresion += tempLongitud + " = heap[(int)" + tempPosArrHeap + "];\n"
                self.ref = tempLongitud
            #print(simbolo.dimensiones[len(self.arreglo.accesoArreglo)])
        return self.expresion

    def calcTam(self):
        return 0
