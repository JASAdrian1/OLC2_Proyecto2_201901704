import re

from Compilador import generador
from Compilador.Expresiones.primitivo import Primitivo
from Compilador.Interfaces.nodo import Nodo
from Compilador.TablaSimbolo.tipo import tipo


class Println(Nodo):
    def __init__(self,token,idnodo,cadena,valores,linea,columna):
        super().__init__(token,idnodo)
        self.cadena = cadena
        self.valores = valores
        self.linea = linea
        self.columna = columna


    def crearTabla(self,ts):
        pass
        #ARREGLAR PARA QUE EN LA TABLA DE SIMBOLOS SE TOME EN CUENTA LAS CADENAS QUE NO SE GUARDAN PARA LA POS DEL HEAP
        #if self.cadena.tipo.tipo_enum == tipo.STR or self.cadena.tipo.tipo_enum == tipo.STRING:
        #    self.cadena.crearTabla(ts)  # Se llama la funcion unicamente para modificar el valor del heap en la tabla simbolos

    def crearCodigo3d(self,ts):
        if self.valores is not None:
            copia_cadena_original = self.cadena
            llaves_cadena = re.findall(r'{}',self.cadena)
            llaves_cadena_array = re.findall(r'{:\?}',self.cadena)
            if len(self.valores) == len(llaves_cadena) + len(llaves_cadena_array):
                cadenaActual = ""
                for i in range(0,len(copia_cadena_original)):
                    cadenaActual = cadenaActual + str(copia_cadena_original[i])
                    print("wwww ",cadenaActual)
                    if copia_cadena_original[i] == "{":     #Se verifica si se quiere imprimir un valor de la lista
                        if i<len(copia_cadena_original)-1:
                            if copia_cadena_original[i+1] =="}":
                                if len(cadenaActual)>2:
                                    cadenaActual = cadenaActual[0:-1]
                                    simbCadenaActual = Primitivo(self.token,-1,cadenaActual,"STR",self.linea,self.cadena)
                                    #Primero se genera la impresion de la cadena que se lleva hasta el momento
                                    self.expresion += self.generarCodigoImpresion(simbCadenaActual,ts)
                                #Posteriormente se genera la impresion del contenido de la variable
                                self.expresion += self.generarCodigoImpresion(self.valores[0],ts)
                                del self.valores[0]
                                cadenaActual = ""
        else:
            self.expresion += self.cadena.crearCodigo3d(ts)
            self.expresion += "P = P + 0;\n"
            self.expresion += "stack[(int)P] = " + str(self.cadena.ref) + ";\n"
            self.expresion += "imprimir();\n"
            self.expresion += "P = P - 0;\n"

        self.expresion += "printf(\"%c\",10);\n"
        return self.expresion


    #Funcion que retorna cadena con la instruccion 3d de la impresion de un valor
    def generarCodigoImpresion(self,valor,ts):
        cadena = ""
        valor.crearCodigo3d(ts)
        cadena += valor.expresion
        #print("--",valor.id)
        print("--",valor.tipo)
        print("--",valor)
        print("--",valor.tipo.tipo_enum)
        if valor.tipo.tipo_enum == tipo.ARRAY or valor.tipo.tipo_enum == tipo.VEC:
            valor.tipo.tipo_enum = valor.tipo.tipoElementos.tipo_enum
            tipoValor = valor.tipo.tipoElementos.tipo_enum
            print("GGGGGG ",valor.tipo.tipo_enum)
        else:
            tipoValor = valor.tipo.tipo_enum

        if tipoValor == tipo.I64 or tipoValor == tipo.BOOL:
            cadena += "printf(\"%d\",(int)"+str(valor.ref) + ");\n"
        elif tipoValor == tipo.F64:
            cadena += "printf(\"%f\","+ str(valor.ref) + ");\n"
        elif tipoValor == tipo.CHAR:
            cadena += "printf(\"%c\",(int)" + str(valor.ref) + ");\n"
        elif tipoValor == tipo.STR or tipoValor == tipo.STRING:
            valor.crearTabla(ts)    #Se llama la funcion unicamente para modificar el valor del heap en la tabla simbolos
            cadena += "P = P + 0;\n"
            cadena += "stack[(int)P] = " + str(valor.ref) + ";\n"
            cadena += "imprimir();\n"
            cadena += "P = P - 0;\n"
        return cadena




    def calcTam(self):
        return 0


def funcionImprimirCadena():
    codigoGenerado = ""
    etiImprimendo = []
    etiSalida = []


    etiImprimendo.append(generador.nuevaEtiqueta())
    etiSalida.append(generador.nuevaEtiqueta())

    tempPosString = generador.nuevoTemporal()
    tempValString = generador.nuevoTemporal()
    tempFin = generador.nuevoTemporal()

    codigoGenerado += "\n\nvoid imprimir(){\n"
    codigoGenerado += tempPosString + " = stack[(int)P];\n"
    codigoGenerado += tempValString + " = heap [(int)" + tempPosString + "];\n"
    codigoGenerado += tempFin + " = - 1;\n"

    codigoGenerado += generador.soltarEtiqueta(etiImprimendo)
    codigoCondicion = tempValString + " == " + tempFin
    codigoGenerado += "if (" + codigoCondicion + ")" + generador.generarGoto(etiSalida[0])
    codigoGenerado += "printf(\"%c\", (int)" + tempValString + ");\n"
    codigoGenerado += tempPosString + " = " + tempPosString + " + 1;\n"
    codigoGenerado += tempValString + " = heap[(int)" + tempPosString + "];\n"
    codigoGenerado += generador.generarGoto(etiImprimendo[0])
    codigoGenerado += generador.soltarEtiqueta(etiSalida)
    codigoGenerado += "return;\n}\n"

    return codigoGenerado

