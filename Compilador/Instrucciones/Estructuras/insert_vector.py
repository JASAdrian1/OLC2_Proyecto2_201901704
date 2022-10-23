from Compilador import generador
from Compilador.Interfaces.nodo import Nodo


class Insert_Vector(Nodo):
    def __init__(self,token,idnodo,id,posicion,valor,linea,columna):
        super().__init__(token,idnodo)
        self.id = id
        self.posicion = posicion
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
        etiSalida2 = [generador.nuevaEtiqueta()]

        self.posicion.crearCodigo3d(ts)
        self.expresion += self.posicion.expresion
        tempPosInsert = generador.nuevoTemporal()
        self.expresion += tempPosInsert + " = " + str(self.posicion.ref) + " - 1;\n"

        self.valor.crearCodigo3d(ts)
        self.expresion += self.valor.expresion

        tempPosValor = generador.nuevoTemporal()
        tempValor = generador.nuevoTemporal()
        tempElemRecorridos = generador.nuevoTemporal()

        self.expresion += tempPosValor + " = " + tempPosArrHeap + " + 1;\n"
        self.expresion += tempElemRecorridos + " = 0;\n"
        self.expresion += "if (" + tempPosInsert + " != -1)" + generador.generarGoto(etiInicio[0])
        tempValorAcutal = generador.nuevoTemporal()
        self.expresion += tempValorAcutal + " = " + tempPosArrHeap + ";\n"
        self.expresion += "stack[(int)" + tempPosicionArr + "] = H;\n"
        self.expresion += "heap[(int)H] = " + str(self.valor.ref) + ";\n"
        self.expresion += generador.generarAumentoHeap()
        self.expresion += "heap[(int)H] = " + tempValorAcutal + ";\n"
        self.expresion += generador.generarAumentoHeap()
        self.expresion += generador.generarGoto(etiSalida2[0])
        self.expresion += generador.soltarEtiqueta(etiInicio)

        self.expresion += "if (" + tempPosInsert + " == " + tempElemRecorridos + ") " + generador.generarGoto(etiSalida[0])
        self.expresion += tempPosValor + " = heap[(int)" + tempPosValor + "];\n"
        self.expresion += tempPosValor + " = " + tempPosValor + " + 1;\n"
        self.expresion += tempElemRecorridos + " = " + tempElemRecorridos + " + 1;\n"
        self.expresion += generador.generarGoto(etiInicio[0])
        self.expresion += generador.soltarEtiqueta(etiSalida)

        #Se almacena en nuevo temporal el valor del siguiente elemento del vector antes de ser modificado
        tempSiguienteVal = generador.nuevoTemporal()
        self.expresion +=tempSiguienteVal + " = heap[(int)" + tempPosValor + "];\n"
        self.expresion += tempSiguienteVal + " = " + tempSiguienteVal + ";\n"

        self.expresion += "heap[(int)" + tempPosValor + "] = H;\n"
        self.expresion += "heap[(int)H] = " + str(self.valor.ref) + ";\n"
        self.expresion += generador.generarAumentoHeap()
        self.expresion += "heap[(int)H] = " + tempSiguienteVal + ";\n"
        self.expresion += generador.generarAumentoHeap()


        self.expresion += generador.soltarEtiqueta(etiSalida2)

        return self.expresion



    def calcTam(self):
        return 0