import tkinter
import tkinter as tk
from tkinter import ttk,messagebox
from PIL import ImageTk, Image

from Analizador.gramatica import analizar_entrada
from Compilador.Entorno import entorno
from Compilador.Entorno.entorno import Entorno,mostrarSimbolos,tabla_simbolos_global,mostrarTablaGlobal
from Compilador import generador
from Compilador.Instrucciones import println


class Ventana:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Compilador")
        self.ventana.geometry("1200x500")
        #self.ventana.rowconfigure(0,minsize=300,weight=0)
        #self.ventana.columnconfigure(1,minsize=600,weight=1)
        self.createWidgets()
        self.ventana.mainloop()

    def createWidgets(self):
        #CUADROS DE TEXTO
        self.text_editor = tk.Text(self.ventana,width=62, height=20)
        self.text_console = tk.Text(self.ventana, width=62, height=20)

        self.text_console.place(x=640,y=50)
        self.text_editor.place(x=60,y=50)



        #BOTONES
        frameBotones = tk.Frame(self.ventana)
        frameBotones.pack(fill="x", side="top")

        botonCompilar = tk.Button(frameBotones,text="Compilar",command=lambda:(self.compilar()))
        botonEditor = tk.Button(frameBotones,text="Editor")
        cbcReportes = ttk.Combobox(
            frameBotones,
            state="readonly",
            values=["Reporte de simbolos","Reporte de errores"]
        )
        cbcReportes.set("Reportes")
        botonReporte = tk.Button(frameBotones, text="Crear reporte", command=lambda:(self.crearReporte(cbcReportes.get())))
        botonAcerca = tk.Button(frameBotones,text="Acerca de", command=lambda:(self.mostrarInfo()))
        botonBorrarConsola = tk.Button(frameBotones, text="Limpiar consola", command=lambda:(self.limpiarConsola()))

        botonEditor.pack(side="left")
        botonCompilar.pack(side="left")
        cbcReportes.pack(side="left")
        botonReporte.pack(side="left")
        botonAcerca.pack(side="left")
        botonBorrarConsola.pack(side="left")

    def compilar(self):
        self.text_console.delete("1.0",tk.END)
        input = self.text_editor.get(0.1, tk.END)
        nodos = analizar_entrada(input)

        sup = Entorno("global", None)
        entorno.tabla_simbolos_global = []
        #print(generador.codigoGenerado)
        #self.text_console.insert("0.1", generador.codigoGenerado)

        #self.text_console.insert("0.1", nodos.crearCodigo3d(ts))

        for nodo in nodos:
            nodo.crearTabla(sup)
        mostrarTablaGlobal()
        #mostrarSimbolos(sup)
        header = "#include <stdio.h>\n"
        header += "float stack[100000];\n"
        header += "float heap[100000];\n"
        header += "float P;\n"
        header += "float H;\n"
        codigo3d = ""
        for nodo in nodos:
            codigo3d += nodo.crearCodigo3d(sup)

        funcionImprimir = println.funcionImprimirCadena()       #Se genera la funcion para imprimir cadenas
        header += generador.generarListaTemporales() + "\n"
        codigo3d = header + codigo3d + funcionImprimir
        self.text_console.insert("0.1", codigo3d)






    def mostrarInfo(self):
        tkinter.messagebox.showinfo("Acerca de","201901704\nJosé Adrian Aguilar Sánchez \n Seccion D")

    def limpiarConsola(self):
        self.text_editor.delete('1.0', tk.END)

