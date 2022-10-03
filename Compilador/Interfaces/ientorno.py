from abc import ABC, abstractmethod



class IEntorno(ABC):
    @abstractmethod
    def put(self, identificador, simbolo):
        pass
    def get(self, identificador):
        pass

