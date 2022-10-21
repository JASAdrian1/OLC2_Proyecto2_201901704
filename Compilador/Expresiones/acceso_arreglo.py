from Compilador import generador
from Compilador.Interfaces.nodo import Nodo
from Compilador.TablaSimbolo.tipo import Tipo, tipo


class Acceso_Arreglo(Nodo):
    def __init__(self,token,idnodo,id,accesoArreglo,linea,columna,nuevoValor=None):
        super().__init__(token,idnodo)
        self.id = id
        self.accesoArreglo = accesoArreglo
        self.linea = linea
        self.columna = columna
        self.nuevoValor = nuevoValor


    def crearTabla(self,ts):
        simbolo = ts.get(self.id)
        print("TIPO: ",simbolo.tipo_dato)
        self.tipo = Tipo(simbolo.tipo_dato.tipo_string)

    def crearCodigo3d(self,ts):
        simbolo = ts.get(self.id)
        self.tipo = simbolo.tipo_dato
        self.tipo.tipoElementos = simbolo.tipo_elementos
        if simbolo.tipo_dato.tipo_enum == tipo.ARRAY:
            print("FF",simbolo, " -- ",self.id)
            print(simbolo.tipo_dato)
            print(simbolo.tipo_elementos)
            print(self.tipo)
            print(simbolo.dimensiones)
            print(simbolo.direccionRel)
            print(simbolo.tipo_elementos)
            #print(self.accesoArreglo)
            #print(simbolo.dimensiones)
            #print(simbolo.dimensiones[1])

            tempPosicionArr = generador.nuevoTemporal()
            self.expresion += tempPosicionArr + " = P + " + str(simbolo.direccionRel) + ";\n"

            tempPosArrHeap = generador.nuevoTemporal()
            self.expresion += tempPosArrHeap + " = stack[(int)"+tempPosicionArr + "];\n"

            print(self.id)
            print(self.accesoArreglo)
            print(simbolo.dimensiones)
            print(simbolo.direccionRel)
            if len(self.accesoArreglo) == len(simbolo.dimensiones):
                posTempValor = generador.nuevoTemporal()
                tempValor = generador.nuevoTemporal()
                self.expresion += posTempValor + " = " + tempPosArrHeap + " + " + str(len(simbolo.dimensiones)) + ";\n"

                for dimension in self.accesoArreglo:
                    dimension.crearCodigo3d(ts)
                    self.expresion += dimension.expresion

                if len(self.accesoArreglo) == 1:
                    self.expresion += posTempValor + " = " + posTempValor + " + " + str(self.accesoArreglo[0].ref) + ";\n"

                elif len(self.accesoArreglo) == 2:
                    tempPosSizeP = generador.nuevoTemporal()
                    tempPosSizeQ = generador.nuevoTemporal()
                    tempValSizeP = generador.nuevoTemporal()
                    tempValSizeQ = generador.nuevoTemporal()

                    valTemp1 = generador.nuevoTemporal()
                    valTemp2 = generador.nuevoTemporal()

                    self.expresion += tempPosSizeP + " = " + tempPosArrHeap + " + 0;\n"
                    self.expresion += tempValSizeP + " = heap[(int)" + tempPosSizeP + "];\n"
                    self.expresion += tempPosSizeQ + " = " + tempPosArrHeap + " + 1;\n"
                    self.expresion += tempValSizeQ + " = heap[(int)" + tempPosSizeQ + "];\n"

                    self.expresion += valTemp1 + " = " + str(self.accesoArreglo[0].ref) + " * " + tempValSizeQ + ";\n"
                    self.expresion += valTemp2 + " = " + valTemp1 + " + " + str(self.accesoArreglo[1].ref) + ";\n"

                    self.expresion += posTempValor + " = " + str(posTempValor) + " + " + valTemp2 + ";\n"

                else:
                    tempPosSizeP = generador.nuevoTemporal()
                    tempPosSizeQ = generador.nuevoTemporal()
                    tempPosSizeR = generador.nuevoTemporal()
                    tempValSizeP = generador.nuevoTemporal()
                    tempValSizeQ = generador.nuevoTemporal()
                    tempValSizeR = generador.nuevoTemporal()

                    valTemp1 = generador.nuevoTemporal()
                    valTemp2 = generador.nuevoTemporal()
                    valTemp3 = generador.nuevoTemporal()
                    valTemp4 = generador.nuevoTemporal()
                    valTemp5 = generador.nuevoTemporal()

                    self.expresion += tempPosSizeP + " = " + tempPosArrHeap + " + 0;\n"
                    self.expresion += tempValSizeP + " = heap[(int)" + tempPosSizeP + "];\n"
                    self.expresion += tempPosSizeQ + " = " + tempPosArrHeap + " + 1;\n"
                    self.expresion += tempValSizeQ + " = heap[(int)" + tempPosSizeQ + "];\n"
                    self.expresion += tempPosSizeR + " = " + tempPosArrHeap + " + 2;\n"
                    self.expresion += tempValSizeR + " = heap[(int)" + tempPosSizeR + "];\n"

                    self.expresion += valTemp1 + " = " + tempValSizeQ + " * " + tempValSizeR + ";\n"
                    self.expresion += valTemp2 + " = " + str(self.accesoArreglo[0].ref) + " * " + valTemp1 + ";\n"
                    self.expresion += valTemp3 + " = " + str(self.accesoArreglo[1].ref) + " * " + tempValSizeR + ";\n"
                    self.expresion += valTemp4 + " = " + valTemp2 + " + " + valTemp3 + ";\n"
                    self.expresion += valTemp5 + " = " + valTemp4 + " + " + str(self.accesoArreglo[2].ref) + ";\n"
                    self.expresion += posTempValor + " = " + str(posTempValor) + " + " + valTemp5 + ";\n"

                if self.nuevoValor is None:
                    self.expresion += tempValor + " = " + "heap[(int)" + posTempValor + "];\n"
                    self.ref = tempValor
                else:
                    self.nuevoValor.crearCodigo3d(ts)
                    self.expresion += self.nuevoValor.expresion
                    self.expresion += "heap[(int)" + posTempValor + "] = " + str(self.nuevoValor.ref) + ";\n"

            else:
                print("22222222222 ",self.id)
                self.expresion += "//***ERROR***Las dimension del acceso no coinciden con la declaracion del arreglo"


        #*******EN DADO CASO SE ESTE ACCIENDO A UN VECTOR SE EJECUTA EL SIGUIENTE CODIGO
        elif tipo.VEC == self.tipo.tipo_dato.tipo_enum:
            print("Accediendo a vector")
            print(self.accesoArreglo)

            tempPosicionArr = generador.nuevoTemporal()
            self.expresion += tempPosicionArr + " = P + " + str(simbolo.direccionRel) + ";\n"

            tempPosArrHeap = generador.nuevoTemporal()
            self.expresion += tempPosArrHeap + " = stack[(int)" + tempPosicionArr + "];\n"

            etiInicio = [generador.nuevaEtiqueta()]
            etiSalida = [generador.nuevaEtiqueta()]

            self.accesoArreglo[0].crearCodigo3d(ts)
            self.expresion += self.accesoArreglo[0].expresion

            tempPosValor = generador.nuevoTemporal()
            tempValor = generador.nuevoTemporal()
            tempElemRecorridos = generador.nuevoTemporal()

            self.expresion += tempPosValor + " = " + tempPosArrHeap + " + 1;\n"
            self.expresion += tempElemRecorridos + " = 0;\n"
            self.expresion += generador.soltarEtiqueta(etiInicio)
            self.expresion += "if (" + str(self.accesoArreglo[0].ref) + " == " + tempElemRecorridos + ") " + generador.generarGoto(etiSalida[0])
            self.expresion += tempPosValor + " = heap[(int)"+tempPosValor + "];\n"
            self.expresion += tempPosValor + " = " + tempPosValor + " + 1;\n"
            self.expresion += tempElemRecorridos + " = " + tempElemRecorridos + " + 1;\n"
            self.expresion += generador.generarGoto(etiInicio[0])
            self.expresion += generador.soltarEtiqueta(etiSalida)

            self.expresion += tempPosValor + " = " + tempPosValor + " - 1;\n"
            self.expresion += tempValor + " = heap[(int)" + tempPosValor + "];\n"
            self.ref = tempValor

        return self.expresion

    def calcTam(self):
        return 0
