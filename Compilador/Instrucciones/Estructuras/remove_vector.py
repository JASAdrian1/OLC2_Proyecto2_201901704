from Compilador import generador
from Compilador.Expresiones.identificador import Identificador
from Compilador.Interfaces.nodo import Nodo


class Remove_Vector(Nodo):
    def __init__(self,token,idnodo,id,posicion,linea,columna):
        super().__init__(token,idnodo)
        self.id = id
        self.posicion = posicion
        self.linea = linea
        self.columna = columna


    def crearTabla(self,ts):
        pass


    def crearCodigo3d(self,ts):
        self.expresion += "//remove vector\n"
        print(self.posicion)

        if isinstance(self.id,Identificador):
            self.id = self.id.id
        simbolo = ts.get(self.id)
        self.tipo = simbolo.tipo_elementos
        print(self.id)

        tempPosicionArr = generador.nuevoTemporal()
        self.expresion += tempPosicionArr + " = P + " + str(simbolo.direccionRel) + ";\n"

        tempPosArrHeap = generador.nuevoTemporal()
        self.expresion += tempPosArrHeap + " = stack[(int)" + tempPosicionArr + "];\n"

        etiInicio = [generador.nuevaEtiqueta()]
        etiSalida = [generador.nuevaEtiqueta()]
        etiSalida2 = [generador.nuevaEtiqueta()]

        self.posicion.crearCodigo3d(ts)
        self.expresion += self.posicion.expresion
        tempPosRemove = generador.nuevoTemporal()
        self.expresion += tempPosRemove + " = " + str(self.posicion.ref) + " - 1;\n"

        tempPosValor = generador.nuevoTemporal()
        tempElemRecorridos = generador.nuevoTemporal()
        tempAnteriorVal = generador.nuevoTemporal()
        tempValRef = generador.nuevoTemporal()

        self.expresion += tempPosValor + " = " + tempPosArrHeap + " + 1;\n"
        self.expresion += tempAnteriorVal + " = " + tempPosValor + ";\n"
        self.expresion += tempElemRecorridos + " = 0;\n"

        self.expresion += "if (" + tempPosRemove + " != -1)" + generador.generarGoto(etiInicio[0])
        tempValorSiguiente = generador.nuevoTemporal()
        self.expresion += tempValorSiguiente + " = " + tempPosArrHeap + " + 1;\n"
        self.expresion += tempValRef + " = heap[(int)"+tempPosArrHeap + "];\n"
        #self.expresion += tempValorSiguiente + " = " +tempValorSiguiente + " + 1;\n"
        self.expresion += tempValorSiguiente + " = " + "heap[(int)" + tempValorSiguiente + "];\n"
        self.expresion += "stack[(int)" + tempPosicionArr + "] = " + tempValorSiguiente + ";\n"
        self.expresion += generador.generarGoto(etiSalida2[0])

        self.expresion += generador.soltarEtiqueta(etiInicio)
        self.expresion += "if (" + tempPosRemove + " == " + tempElemRecorridos + ") " + generador.generarGoto(etiSalida[0])
        self.expresion += tempAnteriorVal + " = " + tempPosValor + ";\n"
        self.expresion += tempPosValor + " = heap[(int)" + tempPosValor + "];\n"
        self.expresion += tempPosValor + " = " + tempPosValor + " + 1;\n"
        self.expresion += tempElemRecorridos + " = " + tempElemRecorridos + " + 1;\n"
        self.expresion += generador.generarGoto(etiInicio[0])
        self.expresion += generador.soltarEtiqueta(etiSalida)

        # Se almacena en nuevo temporal el valor del siguiente elemento del vector antes de ser modificado
        tempSiguienteVal = generador.nuevoTemporal()
        tempValorActual = generador.nuevoTemporal()

        self.expresion += tempValorActual + " = heap[(int)" + tempAnteriorVal + "];\n"
        self.expresion += tempSiguienteVal + " = " + tempValorActual + " + 1;\n"
        self.expresion += tempSiguienteVal + " = heap[(int)" + tempSiguienteVal + "];\n"
        self.expresion += tempValRef + " = heap[(int)" + tempSiguienteVal + "];\n"      #Se guarda como referencia el valor que se saca del vector
        self.expresion += tempSiguienteVal + " = " + tempSiguienteVal + " + 1;\n"
        self.expresion += tempSiguienteVal + " = heap[(int)" + tempSiguienteVal + "];\n"
        #self.expresion += tempSiguienteVal + " = " + tempSiguienteVal + " + 1;\n"
        #self.expresion += tempSiguienteVal + " = heap[(int)"+ tempSiguienteVal +"];\n"
        self.expresion += tempValorActual + " = " + tempValorActual + " + 1;\n"
        self.expresion += "heap[(int)" + tempValorActual + "] = "+ tempSiguienteVal +";\n"

        self.expresion += generador.soltarEtiqueta(etiSalida2)


        self.ref = tempValRef
        return self.expresion


    def calcTam(self):
        return 0