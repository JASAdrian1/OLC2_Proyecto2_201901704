from Compilador.Interfaces.nodo import Nodo
from Compilador import generador



class Sentencia_While(Nodo):
    def __init__(self, token, idnodo):
        super().__init__(token, idnodo)

