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
        self.fila = fila
        self.columna = columna
        print("///",self.tipo)


    def crearCodigo3d(self,ts):
        if self.tipo.tipo_enum == tipo.STR or self.tipo.tipo_enum == tipo.STRING:
            tempInicioString = generador.nuevoTemporal()
            #posInicioString = entorno.posHeap
            #print(posInicioString)
            self.expresion += tempInicioString + " = H;\n"
            for caracter in self.valor:
                self.expresion += "heap[(int)H] = " + str(ord(caracter)) + ";\n"
                self.expresion += generador.generarAumentoHeap()
            self.expresion += "heap[(int)H] = -1;\n"        #Se guarda -1 al final para indicar el fin de la cadena
            self.expresion += generador.generarAumentoHeap()
            self.ref = tempInicioString
        elif self.tipo.tipo_enum == tipo.CHAR:
            self.expresion = ""
            self.ref = str(ord(self.nombre))
        else:
            self.expresion = ""
            self.ref = self.nombre
        return self.expresion

    def crearTabla(self,ts):
        if self.tipo.tipo_enum == tipo.STR or self.tipo.tipo_enum == tipo.STRING:
            self.posHeap = entorno.posHeap
            entorno.posHeap += len(self.valor) + 1  # La posicion del heap se desplazara la longitud de la cadena + 1 (por el -1 que se guarda al firal)

    def calcTam(self):
        return 1