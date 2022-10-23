from Compilador import generador
from Compilador.Interfaces.nodo import Nodo
from Compilador.TablaSimbolo.tipo import tipo


class Capacity_Vector(Nodo):
    def __init__(self,token,idnodo,id,linea,columna):
        super().__init__(token,idnodo)
        self.id = id
        self.linea = linea
        self.columna = columna

    def crearTabla(self,ts):
        pass

    def crearCodigo3d(self,ts):
        self.expresion += "//capacity\n"
        simbolo = ts.get(self.id.id)
        print(simbolo)
        print(self.id,"!!!!!!")

        temPosCero = generador.nuevoTemporal()
        tempPosicionArr = generador.nuevoTemporal()
        tempPosArrHeap = generador.nuevoTemporal()

        etiInicio = [generador.nuevaEtiqueta()]
        etiInicio2 = [generador.nuevaEtiqueta()]
        etiSalida = [generador.nuevaEtiqueta()]

        tempPosValor = generador.nuevoTemporal()
        tempSiguienteDir = generador.nuevoTemporal()
        tempLongitud = generador.nuevoTemporal()

        self.expresion += tempLongitud + " = 0;\n"
        # OBTENCION DEL POSICION DEL VECTOR ALMACENADO EN EL STACK
        self.expresion += tempPosicionArr + " = P + " + str(simbolo.direccionRel) + ";\n"
        self.expresion += tempPosArrHeap + " = stack[(int)" + tempPosicionArr + "];\n"

        # SE ALMACENA EN UN TEMPORAL LA POSICION EN EL HEAP DONDE SE ALMACENA LA DIRECCION DEL SIGUIENTE ELEMENTO
        self.expresion += tempPosValor + " = " + tempPosArrHeap + ";\n"
        self.expresion += temPosCero + " = " + tempPosValor + "+1;\n"
        self.expresion += temPosCero + " = heap[(int)" + temPosCero + "];\n"
        self.expresion += tempSiguienteDir + " = heap[(int)" + tempPosValor + "];\n"  # Se almacena la direccion del siguiente arreglo

        self.expresion += generador.soltarEtiqueta(etiInicio2)
        self.expresion += "if (" + temPosCero + " != 0) " + generador.generarGoto(etiInicio[0])  # Si la direccion del siguiente es 0 es que aun no se inicializa el siguiente vector
        self.expresion += tempPosValor + " = " + tempPosValor + " + 2;\n"
        self.expresion += temPosCero + " = " + tempPosValor + " + 1;\n"
        self.expresion += temPosCero + " = heap[(int)" + temPosCero + "];\n"
        self.expresion += tempLongitud + " = " + tempLongitud + " + 1;\n"
        self.expresion += generador.generarGoto(etiInicio2[0])

        self.expresion += generador.soltarEtiqueta(etiInicio)
        self.expresion += "if (" + temPosCero + " == -1) " + generador.generarGoto(
            etiSalida[0])  # Si la posicion del siguiente valor es -1 significa que es el final del vector
        self.expresion += tempPosValor + " = " + tempPosValor + " + 1;\n"
        self.expresion += temPosCero + " = heap[(int)" + tempPosValor + "];\n"
        self.expresion += tempLongitud + " = " + tempLongitud + " + 1;\n"
        self.expresion += generador.generarGoto(etiInicio2[0])

        self.expresion += generador.soltarEtiqueta(etiSalida)
        self.ref = tempLongitud

        return self.expresion

    def calcTam(self):
        return 0
