import re

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

    def crearCodigo3d(self,ts):
        if self.valores is not None:
            copia_cadena_original = self.cadena
            llaves_cadena = re.findall(r'{}',self.cadena)
            llaves_cadena_array = re.findall(r'{:\?}',self.cadena)
            if len(self.valores) == len(llaves_cadena) + len(llaves_cadena_array):
                for i in range(0,len(copia_cadena_original)):
                    if copia_cadena_original[i] == "{":     #Se verifica si se quiere imprimir un valor de la lista
                        if i<len(copia_cadena_original)-1:
                            if copia_cadena_original[i+1] =="}":
                                self.expresion += self.generarCodigoImpresion(self.valores[0],ts)
                                del self.valores[0]
        else:
            copia = self.cadena
            copia = copia[1:-1]
            for caracter in copia:
                self.expresion += "printf(\"%c\"," + str(ord(caracter)) + ");\n"

        self.expresion += "printf(\"%c\",10);\n"
        return self.expresion


    #Funcion que retorna cadena con la instruccion 3d de la impresion de un valor
    def generarCodigoImpresion(self,valor,ts):
        cadena = ""
        valor.crearCodigo3d(ts)
        cadena += valor.expresion
        if valor.tipo.tipo_enum == tipo.I64 or valor.tipo.tipo_enum == tipo.BOOL:
            cadena += "printf(\"%d\",(int)"+valor.ref + ");\n"
        elif valor.tipo.tipo_enum == tipo.F64:
            cadena += "printf(\"%f\","+valor.ref + ");\n"
        return cadena




    def calcTam(self):
        return 0


def imprimirCadena():
    pass