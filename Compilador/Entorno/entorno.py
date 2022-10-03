


class Entorno:
    def __init__(self, nombre, entornoAnterior=None):
        self.nombre = nombre
        self.tablaSimbolos = {}
        self.entornoAnterior = entornoAnterior


    def put(self,listaid, simbolo):
        for id in listaid:
            for simb in self.tablaSimbolos:
                if id in simb:
                    print("ERROR. Ya se encuentra el id en la tabla simbolos")
                    return
            self.tablaSimbolos[id] = simbolo
            print(self.tablaSimbolos)

    def get(self, id):
        simbolo = None
        entorno = self
        while entorno is not None:
            if id in entorno.tablaSimbolos:
                return entorno.tablaSimbolos[id]
            entorno = entorno.entornoAnterior
        print("La variable no se ha encontrado (entorno)")
        return None

def mostrarSimbolos(entorno):
    for simb in entorno.tablaSimbolos:
        print("Identificador: ",entorno.tablaSimbolos[simb].id,end="\t")
        print("Tipo: ",entorno.tablaSimbolos[simb].tipo,end="\t")
        print("Direccion: ",entorno.tablaSimbolos[simb].direccion)

    def agregarVariable(self, id, valor, tipo, tipoSimbolo, tablaSimbolo=None):
        nuevoSimbolo = {'valor':valor, 'tipo': tipo, 'tipoSimbolo':tipoSimbolo, 'tablaSimbolo': tablaSimbolo}

