from Compilador import generador
from Compilador.Interfaces.nodo import Nodo


class Sentencia_If(Nodo):
    def __init__(self,token, idnodo, condicion, instruccionesif,instruccioneselse):
        super().__init__(token,idnodo)
        self.condicion = condicion
        self.instruccionesif = instruccionesif
        self.instruccioneselse = instruccioneselse
        self.etiSalida = []

    def crearTabla(self,ts):
        pass

    def crearCodigo3d(self,ts):
        self.expresion += self.condicion.crearCodigo3d(ts)
        self.expresion += generador.soltarEtiqueta(self.condicion.etiV) #SE MUESTRAN LAS ETIQUETAS VERDADERAS

        #<---- EN ESTE ESPACIO DE AQUI SE DEBERIA GENERA EL CODIGO DE LAS INSTRUCCIONES----->
        self.expresion += "//CODIGO GENERADO POR LAS INSTRUCCIONES DENTRO DE IF\n"
        for instruccion in self.instruccionesif:
            instruccion.crearCodigo3d(ts)
            self.expresion += instruccion.expresion

        self.etiSalida.append(generador.nuevaEtiqueta())  #SE GENERA UNA ETIQUETA PARA SALIR DE LA INSTRUCCION IF
        self.expresion += "goto " + self.etiSalida[0] + "\n"  #SE MUESTRAN LAS ETIQUETAS DE LA CONDICION FALAS
        self.expresion += generador.soltarEtiqueta(self.condicion.etiF)

        # <---- EN ESTE ESPACIO DE AQUI SE DEBERIA GENERA EL CODIGO DE LAS INSTRUCCIONES ELSE----->
        self.expresion += "//CODIGO GENERADO POR LAS INSTRUCCIONES DENTRO DE ELSE EN CASO EXISTA\n"
        if self.instruccioneselse is not None:
            for instruccion in self.instruccioneselse:
                instruccion.crearCodigo3d(ts)
                self.expresion += instruccion.expresion


        self.expresion += generador.soltarEtiqueta(self.etiSalida)
        return self.expresion