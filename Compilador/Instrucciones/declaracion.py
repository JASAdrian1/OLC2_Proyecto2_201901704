from Compilador.Entorno import entorno
from Compilador.Entorno.simbolo import Simbolo
from Compilador.Interfaces.nodo import Nodo
from Compilador import generador


class Declaracion(Nodo):
    def __init__(self,token, idnodo, id, valor):
        super().__init__(token,idnodo)
        self.id = id
        self.valor = valor

    def crearTabla(self,ts):
        for id in self.id:
            nuevoSimbolo = Simbolo(id, self.valor, entorno.desplazamiento)
            ts.put(id, nuevoSimbolo)
            entorno.desplazamiento += 1

    def crearCodigo3d(self,ts):
        self.expresion += "//Realizando declaracion"+"\n"
        return self.expresion