

class Condicion:
    def __init__(self, etiVerdaderas=None, etiFalsas=None):
        self.etiVerdaderas = []
        self.etiFalsas = []
        self.expresion = ""
        if etiVerdaderas is not None:
            self.etiVerdaderas.append(etiVerdaderas)
        if etiFalsas is not None:
            self.etiFalsas.append(etiFalsas)


    def crearCodigo3d(self,ts):
        pass
