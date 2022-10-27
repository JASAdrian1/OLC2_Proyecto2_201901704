from Compilador.Entorno import entorno
from Compilador.Entorno.simbolo import Simbolo
from Compilador.Interfaces.nodo import Nodo
from Compilador.TablaSimbolo.tipo import tipo


class Sentencia_Return(Nodo):
    def __init__(self,token,idnodo,valorRetornado,linea,columna):
        super().__init__(token,idnodo)
        self.valorRetornado = valorRetornado
        self.linea = linea
        self.columna = columna

    def crearTabla(self,ts):
        simboloFuncion = ts.get(ts.funcionEnEjecucion,"funcion")
        print("Funcion: ",ts.funcionEnEjecucion)
        print(simboloFuncion.tipo_dato)
        size = 0
        if self.valorRetornado is not None:
            if simboloFuncion.tipo_dato is not None:
                print(simboloFuncion.tipo_dato.tipo_enum)
                tipo_return = simboloFuncion.tipo_dato.tipo_enum
                if tipo_return == tipo.I64 or tipo_return == tipo.F64 or tipo_return == tipo.BOOL or tipo_return == tipo.CHAR or tipo_return == tipo.USIZE:
                    size = 1
                simboloReturn = Simbolo("return",simboloFuncion.tipo_dato,"variable",size,ts.nombre,0,-1,self.linea,self.columna)
                ts.put("return", simboloReturn)
                entorno.tabla_simbolos_global.append(simboloReturn)

            else:
                print("***ERROR***Se esta retornando un valor en una funcion void")

    def crearCodigo3d(self,ts):
        if self.valorRetornado == None:
            self.expresion += "return;\n"
        else:
            self.valorRetornado.crearCodigo3d(ts)
            self.expresion += self.valorRetornado.expresion

            self.expresion += "stack[(int)P] = " + str(self.valorRetornado.ref) + ";\n"


        return self.expresion


    def calcTam(self):
        return 1