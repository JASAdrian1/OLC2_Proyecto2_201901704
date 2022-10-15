from Compilador.Expresiones.identificador import Identificador

desplazamiento = 0
posHeap = 0
tabla_simbolos_global = []

class Entorno:
    def __init__(self, nombre, entornoAnterior=None):
        self.nombre = []
        self.tablaSimbolos = {}
        self.entornoAnterior = entornoAnterior
        self.listaEtiquetas = []
        self.funcionEnEjecucion = ""

        ent = entornoAnterior
        if ent is not None:
            self.nombre.append(ent.nombre)
            ent = ent.entornoAnterior
        self.nombre.append(nombre)


    def put(self,id, simbolo):
        for simb in self.tablaSimbolos:
            if id == simb:
                print(id)
                #print(self.get(id).tipo_simbolo+ "=="+ simbolo.tipo_simbolo)
                print(id)
                if self.get(id).tipo_simbolo == simbolo.tipo_simbolo:
                    print("ERROR. Ya se encuentra el id en la tabla simbolos")
                    return
        print("Se ha agregado la variable a la tabla simbolos")
        self.tablaSimbolos[id] = simbolo
        #print(self.tablaSimbolos)

    def get(self, id, tipoSimbolo = None):
        simbolo = None
        entorno = self
        while entorno is not None:
            if id in entorno.tablaSimbolos:
                if tipoSimbolo is not None:
                    print(tipoSimbolo, " == ",entorno.tablaSimbolos[id].tipo_simbolo)
                    #if tipoSimbolo == entorno.tablaSimbolos[id].tipo_simbolo:
                    return entorno.tablaSimbolos[id]
                else:
                    return entorno.tablaSimbolos[id]
            entorno = entorno.entornoAnterior
        print("La variable no se ha encontrado (entorno)")
        return None


    def getUltimaPosStack(self):
        if len(self.tablaSimbolos)>0:
            if list(self.tablaSimbolos.values())[-1].direccionRel == -1:
                return 1
            else:
                return list(self.tablaSimbolos.values())[-1].direccionRel + 1
        else:
            if self.entornoAnterior is not None:
                ent = self.entornoAnterior
                while ent is not None:
                    if len(self.entornoAnterior.tablaSimbolos) >0:
                        return list(self.entornoAnterior.tablaSimbolos.values())[-1].direccionRel + 1
                    ent = ent.entornoAnterior
                return 0
            else:
                return 0


    def actualizarValorVariable(self):
        codigoGenerado = ""
        for simbolo in tabla_simbolos_global:
            print("Simbolo: ",simbolo.tipo_simbolo)
            print(simbolo.id)
            if simbolo.tipo_simbolo == "parametro":
                if isinstance(simbolo,Identificador):
                    codigoGenerado += simbolo.actualizarReferencia(self.tablaSimbolos)
        return codigoGenerado


    def crearListaNombresEntorno(self):
        if self.entornoAnterior is not None:
            nombres =[]
            nombres = self.entornoAnterior.nombre.copy()
            nombres.append(self.nombre[-1])
            self.nombre = nombres
            print(self.nombre)
        else:
            nombres = []
            nombres.append(self.nombre[-1])
            self.nombre = nombres

def mostrarSimbolos(entorno):
    #Se ordenan los entorno
    ent = entorno
    entornos = []
    while ent is not None:
        entornos.append(ent)
        ent = ent.entornoAnterior
    entornos.reverse()

    #Se imprimen los simbolos de los entornos
    for ent in entornos:
        for simb in ent.tablaSimbolos:
            tipo = "-"
            if ent.tablaSimbolos[simb].tipo_dato is not None:
                tipo = ent.tablaSimbolos[simb].tipo_dato.tipo_string
            print("Identificador: ",ent.tablaSimbolos[simb].id,end="\t")
            print("Tipo: ",tipo,end="\t")
            print("Direccion: ",ent.tablaSimbolos[simb].direccionRel,end="\t")
            print("Entorno: ",','.join(ent.nombre))


    def agregarVariable(self, id, valor, tipo, tipoSimbolo, tablaSimbolo=None):
        nuevoSimbolo = {'valor':valor, 'tipo': tipo, 'tipoSimbolo':tipoSimbolo, 'tablaSimbolo': tablaSimbolo}


def mostrarTablaGlobal():
    print("************************MOSTRANDO TABLA GLOBAL*************************")
    for simb in tabla_simbolos_global:
        tipo = "-"
        if simb.tipo_dato is not None:
            tipo = simb.tipo_dato.tipo_string
        print("Identificador: ", simb.id, end="\t")
        print("Tipo: ", tipo, end="\t")
        print("Tipo simbolo: ",simb.tipo_simbolo, end="\t")
        print("Size: ",simb.size, end="\t")
        print("DireccionRel: ", simb.direccionRel, end="\t")
        print("DireccionAbs: ",simb.direccionAbs, end="\t")
        print("Entorno: ", ','.join(simb.entorno))


def getFuncionTablaGlobal(id):
    for simb in tabla_simbolos_global:
        if simb.id == id:
            if simb.tipo_simbolo == "funcion":
                return simb

    print("Funcion no encontrada en la tabla global")
    return None


def getHeapLibre():
    global posHeap
    heap = posHeap
    posHeap += 1
    return heap


def aumentarHeap():
    global posHeap
    posHeap += 1


