from Compilador import generador
from Compilador.Interfaces.nodo import Nodo
from Compilador.TablaSimbolo.tipo import tipo, Tipo
from Compilador.Entorno import entorno


class Primitivo(Nodo):
    def __init__(self,token,idNodo,valor,tipoValor,fila,columna):
        super().__init__(token,idNodo)
        self.ref = valor
        self.nombre = valor
        self.valor = valor
        self.expresion = ""
        self.posHeap = -1
        self.tipo = Tipo(tipoValor)
        print("///",self.tipo)


    def crearCodigo3d(self,ts):
        if self.tipo.tipo_enum == tipo.STR or self.tipo.tipo_enum == tipo.STRING:
            tempInicioString = generador.nuevoTemporal()
            posInicioString = entorno.posHeap
            print(posInicioString)
            self.expresion += tempInicioString + " = H;\n"
            for caracter in self.valor:
                self.expresion += "heap[(int)H] = " + str(ord(caracter)) + ";\n"
                self.expresion += generador.generarAumentoHeap()
            self.expresion += "heap[(int)H] = -1;\n"        #Se guarda -1 al final para indicar el fin de la cadena
            self.expresion += generador.generarAumentoHeap()
            self.ref = tempInicioString
            self.posHeap = posInicioString
        else:
            self.expresion = ""
            self.ref = self.nombre
        return self.expresion

    def crearTabla(self,ts):
        pass

    def calcTam(self):
        return 1