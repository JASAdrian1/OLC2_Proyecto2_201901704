from Compilador.Interfaces.nodo import Nodo
from Compilador.Entorno.entorno import getFuncionTablaGlobal


class Llamada_funcion_ins(Nodo):
    def __init__(self,token,idnodo,id,parametros,linea,columna):
        super().__init__(token,idnodo)
        self.id = id
        self.parametros = parametros
        self.linea = linea
        self.columna = columna

    def crearTabla(self,ts):
        pass

    def crearCodigo3d(self,ts):
        #Se busca en la tabla la funcion desde la que se ejecutara la llamada de la funcion
        funcionRaiz = getFuncionTablaGlobal(ts.funcionEnEjecucion)

        funcionLlamada = getFuncionTablaGlobal(self.id)
        if funcionLlamada is not None:
            if self.parametros is None:
                self.expresion += "P = P + " + str(funcionRaiz.size) + ";\n"
                self.expresion += self.id + "();\n"
                self.expresion += "P = P - " + str(funcionRaiz.size) + ";\n"

        else:
            print("***ERROR*** La funcion que se esta llamando no de ha declarado, funcion:",self.id)

        return self.expresion

    def calcTam(self):
        return 0
