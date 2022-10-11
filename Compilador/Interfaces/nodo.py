

from abc import ABC, abstractmethod

class Nodo(ABC):
    def __init__(self, token, idNodo):
        self.nombre = token.type
        self.tipo = token.type
        self.valor = token.value
        self.idNodo = idNodo
        self.expresion = ""
        self.ref = ""
        super().__init__()


    @abstractmethod
    def crearCodigo3d(self,ts):
        pass

    @abstractmethod
    def crearTabla(self,ts):
        pass

    @abstractmethod
    def calcTam(self):
        pass

