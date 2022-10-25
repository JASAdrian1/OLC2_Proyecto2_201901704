from Compilador import generador
from Compilador.Expresiones.acceso_arreglo import Acceso_Arreglo
from Compilador.Expresiones.identificador import Identificador
from Compilador.Interfaces.nodo import Nodo
from Compilador.TablaSimbolo.tipo import tipo, Tipo


class Len_Arreglo(Nodo):
    def __init__(self,token,idnodo,arreglo,linea,columna):
        super().__init__(token,idnodo)
        self.arreglo = arreglo
        self.linea = linea
        self.columna = columna
        self.tipo = Tipo("I64")

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

        elif simbolo.tipo_dato.tipo_enum == tipo.VEC:
            etiInicio = [generador.nuevaEtiqueta()]
            etiSalida = [generador.nuevaEtiqueta()]

            tempPosValor = generador.nuevoTemporal()
            tempSiguienteDir = generador.nuevoTemporal()
            tempLongitud = generador.nuevoTemporal()

            self.expresion += tempLongitud + " = 0;\n"
            #OBTENCION DEL POSICION DEL VECTOR ALMACENADO EN EL STACK
            self.expresion += tempPosicionArr + " = P + " + str(simbolo.direccionRel) + ";\n"
            self.expresion += tempPosArrHeap + " = stack[(int)" + tempPosicionArr + "];\n"

            #SE ALMACENA EN UN TEMPORAL LA POSICION EN EL HEAP DONDE SE ALMACENA LA DIRECCION DEL SIGUIENTE ELEMENTO
            self.expresion += tempPosValor + " = " + tempPosArrHeap + ";\n"
            self.expresion += tempSiguienteDir + " = heap[(int)" + tempPosValor + "];\n"  # Se almacena la direccion del siguiente arreglo

            self.expresion += generador.soltarEtiqueta(etiInicio)
            self.expresion += "if (" + tempPosValor + " == -1) " + generador.generarGoto(etiSalida[0])  # Si la posicion del siguiente valor es -1 significa que es el final del vector
            self.expresion += tempPosValor + " = " + tempPosValor + " + 1;\n"
            self.expresion += tempPosValor + " = heap[(int)" + tempPosValor + "];\n"
            self.expresion += "if (" + tempPosValor + " == 0) " + generador.generarGoto(etiSalida[0])  # Si la direccion del siguiente es 0 tambien indica la finalizacion del arreglo
            self.expresion += tempLongitud + " = " + tempLongitud + " + 1;\n"
            self.expresion += generador.generarGoto(etiInicio[0])

            self.expresion += generador.soltarEtiqueta(etiSalida)
            self.ref = tempLongitud



        return self.expresion

    def calcTam(self):
        return 0
