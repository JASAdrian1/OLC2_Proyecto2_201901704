from Compilador.Interfaces.nodo import Nodo



class Declaracion_arreglo(Nodo):
    def __init__(self,token,idnodo,id,valor,tipo,tipoElementos,estructuraArreglos,esMutable,linea,columna):
        super().__init__(token,idnodo)
        self.id = id
        self.valor = valor
        self.tipo = tipo
        self.tipoElementos = tipoElementos
        self.estructuraArreglos = estructuraArreglos
        self.esMutable = esMutable
        self.linea = linea
        self.columna = columna


    