from Compilador import generador
from Compilador.Entorno import simbolo
from Compilador.Interfaces.nodo import Nodo


class Push_Vector(Nodo):
    def __init__(self,token,idnodo,id,valor,linea,columna):
        super().__init__(token,idnodo)
        self.id = id
        self.valor = valor
        self.linea = linea
        self.columna = columna


    def crearTabla(self,ts):
        pass

    def crearCodigo3d(self,ts):
        simbolo = ts.get(self.id)
        tempPosicionArr = generador.nuevoTemporal()
        self.expresion += tempPosicionArr + " = P + " + str(simbolo.direccionRel) + ";\n"

        tempPosArrHeap = generador.nuevoTemporal()
        self.expresion += tempPosArrHeap + " = stack[(int)" + tempPosicionArr + "];\n"

        etiInicio = [generador.nuevaEtiqueta()]
        etiSalida = [generador.nuevaEtiqueta()]

        self.valor.crearCodigo3d(ts)
        self.expresion += self.valor.expresion

        tempPosValor = generador.nuevoTemporal()
        tempSiguienteDir = generador.nuevoTemporal()

        #tempPosArrHeap apunta al primer valor que se tiene guardado del vector
        self.expresion += tempPosValor + " = " + tempPosArrHeap + " + 1;\n"     #Se aumenta 1 para ir al heap donde se guarda la direccion del siguiente arreglo
        self.expresion += tempSiguienteDir + " = heap[(int)" + tempPosValor + "];\n"        #Se almacena la direccion del siguiente arreglo
        self.expresion += generador.soltarEtiqueta(etiInicio)
        self.expresion += "if (" + tempSiguienteDir + " == -1) " + generador.generarGoto(etiSalida[0])  #Si la posicion del siguiente valor es -1 significa que es el final del vector
        self.expresion += tempPosValor + " = " + tempSiguienteDir + " + 1;\n"
        self.expresion += tempSiguienteDir + " = heap[(int)" + tempPosValor + "];\n"
        #self.expresion += tempPosValor + " = heap[(int)" + tempPosValor + "];\n"
        self.expresion += generador.generarGoto(etiInicio[0])
        self.expresion += generador.soltarEtiqueta(etiSalida)

        self.expresion += "heap[(int)" + tempPosValor + "] = H;\n"
        self.expresion += "heap[(int)H] = " + str(self.valor.ref) + ";\n"
        self.expresion += generador.generarAumentoHeap()
        self.expresion += "heap[(int)H] = -1;\n"
        self.expresion += generador.generarAumentoHeap()

        return self.expresion


    def calcTam(self):
        return 0