# ********* PARTE 3: Interfaz grafica UI para validar el modelo *********

from tkinter import *
from keras_preprocessing import image
import numpy as np
import tensorflow as tf
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
from keras.initializers import glorot_uniform
from tkinter import Tk, Label, Button, ttk
import tkinter
import re
from Interfaz_logic import tools
from os import path


longitud, altura = 200, 200 # Configuramos el alto y ancho que tendran las imagenes a utilizar en la interfaz

# Definimos las rutas de los archivos necesarios para que funcione el programa
ruta_logo_itm = 'C:/Users/saulu/Documents/Thesis/Thesis/logo.jpg'
ruta_modelo_default = 'C:/Users/saulu/Documents/Thesis/Thesis/DATOS_RED/Modelo.h5'
ruta_pesos_default = 'C:/Users/saulu/Documents/Thesis/Thesis/DATOS_RED/Pesos.h5'
ruta_img_prueba = 'C:/Users/saulu/Documents/Thesis/Thesis/IMAGENES_PRUEBA'
cont = 0 # variable global que funje como contador para controlar la eliminacion del boton seleccionar otra imagen

# Esta es la clase que crea la interfaz grafica se utiliza POO
class Principal(tools):
    # Metodo constructor el cual recibe un objeto Tk(), este metodo inicializa toda la interfaz
    def __init__(self, master):
        self.master = master
        self.master.title("(TESIS) Predicción de Salud en Corales del Caribe Mexicano")
        self.master.geometry("500x400+450+100")
        self.master.resizable(False, False)
        self.etiqueta_modelo = Label(self.master, text="Seleccione el modelo: ")
        self.etiqueta_modelo.pack()
        self.boton_cargar_modelo = Button(self.master, text="Cargar Modelo", command=self.cargar_modelo) # boton para cargar el modelo obtenido de la red
        self.boton_cargar_modelo.pack()
        self.etiqueta_pesos = Label(self.master, text="Seleccione los pesos: ")
        self.etiqueta_pesos.pack()
        self.boton_cargar_pesos = Button(self.master, text="Cargar Pesos", command=self.cargar_pesos) # boton para cargar los pesos obtenidos de la red
        self.boton_cargar_pesos.pack()
        self.etiqueta_imagen = Label(self.master, text="Seleccione Imagen a Evaluar: ")
        self.etiqueta_imagen.pack()
        self.boton_cargar_imagen = Button(self.master, text="Cargar Imagen", command=self.seleccionar_imagen) # Cargar la imagen que se evaluara
        self.boton_cargar_imagen.pack()
        self.var_img = super().configurar_img(ruta_logo_itm)
        self.panelLogo = Label(self.master, image=self.var_img) # El logo se coloca en una etiqueta_imagen
        self.panelLogo.pack(side="bottom")
        self.master.mainloop()  # Este mainloop es el que mantiene la VENTANA PRINCIPAL FUNCIONANDO

    # Metodo para seleccionar el modelo
    def cargar_modelo(self): 
        self.ruta_modelo_user = super().abrir_ventana()  # llamamos a la funcion de la clase padre para abrir un cuadro de dialogo
        if len(self.ruta_modelo_user) > 0:  # si el tamaño de la cadena es mayor a 0, es que existe la ruta
            if self.ruta_modelo_user != ruta_modelo_default: # si la ruta del usuario es diferente a la ruta por defecto se lanza una ventana de error
                super().ventana_alerta()
            else:
                super().eliminar_widgets(self.etiqueta_modelo, self.boton_cargar_modelo) # si la ruta esta correcta eliminamos los widgets usados
        return self.ruta_modelo_user  # devolvemos la ruta dada por el usuario
    
    # Metodo para seleccionar los pesos
    def cargar_pesos(self):
        self.ruta_pesos_user = super().abrir_ventana()
        if len(self.ruta_pesos_user) > 0: 
            if self.ruta_pesos_user != ruta_pesos_default:
                super().ventana_alerta()
            else:
                super().eliminar_widgets(self.etiqueta_pesos, self.boton_cargar_pesos)
        return self.ruta_pesos_user

    # Metodo para elegir la imagen que sera evaluada
    def seleccionar_imagen(self):
        global cont 
        panel_img_principal = None # esta variable contendra la imagen que se muestra al momento de seleccionar la imagen
        self.ruta_imagen_user = super().abrir_ventana() # Abre una ventana de dialogo para seleccionar una imagen, y devuelve la ruta de la imagen seleccionada
        self.ruta_imagen_split = path.split(self.ruta_imagen_user)

        if len(self.ruta_imagen_user) > 0: # si elige una imagen
            if self.ruta_imagen_split[0] == ruta_img_prueba: # evaluamos que este dentro de la ruta establecida para imagenes de prueba
                if re.search("\.(jpg|jpeg|JPG|png|bmp|tiff)$", self.ruta_imagen_user): # Validamos que el usuario haya seleccionado una imagen
                    super().eliminar_widgets(self.etiqueta_imagen, self.boton_cargar_imagen, self.panelLogo) # limpiamos la GUI
                    if cont > 0: # contador para evualuar el estado al seleccionar otra imagen,si se elige otra imagen, se borra el boton ya que inmediatamente se colocara de nuevo junto con el boton prediccion
                        super().eliminar_widgets(self.boton_selec_otra_img) # la accion es eliminar el boton seleccionar otra imagen

                    self.imagen_configurada = super().configurar_img(self.ruta_imagen_user) # se crea una copia de la imagen para colocarla en la ventana secundaria al momento de predecir
                    self.botonPredict = Button(text="Detectar Estado de Salud", command=self.prediccion) # se crea el boton que hace la prediccion
                    self.botonPredict.pack() # el boton es colocado en la interfaz
                    self.boton_selec_otra_img = Button(text="Seleccionar otra imagen", command=self.abrir_otra_img) # se crea un boton debajo por si quiere seleccionar otra imagen
                    self.boton_selec_otra_img.pack()
                    cont = cont + 1  # al momento de seleccionar la imagen, el contador aumenta en 1, esto representa el primer estado que se pinta en la UI

                    if panel_img_principal is None: # Si la variable panel_img_principal esta inicializada en nula
                        self.panel_img_principal = Label(self.master, image=self.imagen_configurada)  # se carga la imagen en la label
                        self.panel_img_principal.pack(side="bottom")
                else: # si no selecciono una imagen se lanza ventana alerta
                    super().ventana_alerta()
                self.master.mainloop()
            else: # si NO es una imagen
                super().ventana_alerta() # le damos click en aceptar a la ventana
               # super().insertar_widgets(self.boton_selec_otra_img)
            self.master.mainloop() # Este mainloop se coloca aqui para mantener la VENTANA PRINCIPAL FUNCIONANDO despues de cerrar la ventana secundaria del resultado de la prediccion

    # Metodo que funciona cuando el usuario quiera seleccionar otra imagen para evaluar
    def abrir_otra_img(self):
        super().eliminar_widgets(self.panel_img_principal, self.botonPredict) # se limpia la pantalla
        self.seleccionar_imagen()

    # Metodo que funciona para realizar una prediccion 
    def prediccion(self):
        super().eliminar_widgets(self.botonPredict, self.boton_selec_otra_img, self.panel_img_principal) # limpiamos la pantalla
        
        with tf.keras.utils.custom_object_scope({'GlorotUniform':glorot_uniform()}): # cargamos el modelo y los pesos mediante sus rutas
            cnn = load_model(self.ruta_modelo_user)
        cnn.load_weights(self.ruta_pesos_user)

        x = load_img(self.ruta_imagen_user, target_size = (longitud, altura)) # Aqui se hace la prediccion obteniendo la imagen de la ruta y cambiandole su tamaño al tamaño que se uso en el entrenamiento 200x200
        x = img_to_array(x) # la imagen se convierte a tipo arreglo numpy con tres canales por RGB(200,200,3)

        # luego se convierte la imagen a 4D, se agrega un 1 dimension mas en la posicion especificada axis=0, quedando
        # de la siguiente manera (1,200,200,3) en donde este uno representa el tamaño de lote, este formato 4D es necesario
        # para las capas Conv2D de Keras
        x = np.expand_dims(x, axis = 0) # 

        # Aqui se realiza la prediccion si el valor de la prediccion es mayor a el umbral 0.5 entonces la salida
        # será 1, si no la salida sera 0, esto lo devuelve en un arreglo numpy [[0]] o [[1]] dependiendo de la prediccion
        answer = (cnn.predict(x) > 0.5).astype("int32") 
        respuesta = answer[0][0] # Accedemos al valor almacenado en la matriz indexando [0][0] ya que es en 2D
        
        panel_ventana_prediccion = None # variable que almacenara la imagen que ira en la label
        if respuesta == 0: # si la prediccion es 0 == Enfermo
            print(respuesta)
            self.subVentana = Toplevel() # Crea una nueva ventana secundaria para mostrar la salida
            self.subVentana.geometry("600x300+300+150") # Se establece el tamaño de la ventana secundaria
            self.subVentana.wm_title("(Tesis)Información Sobre Estado de Salud") # Se le asigna el titulo
            self.subVentana.focus_set() # Este metodo enfoca la ventana secundaria 
            self.subVentana.grab_set() # desactivamos la ventana principal 
            self.pred = Label(self.subVentana, text = "Coral ENFERMO detectado") # asignamos la etiqueta_imagen para mencionar que es un coral enfermo
            self.pred.grid(row = 0, column = 0)
            self.pred.config(fg = "black", font = ("verdana", 12))
           
            if panel_ventana_prediccion == None:
                self.panel_ventana_prediccion = Label(self.subVentana, image = self.imagen_configurada) # le pasamos la imagen a la etiqueta_imagen
                self.panel_ventana_prediccion.grid(row = 1, column = 0) # posicionamos la etiqueta_imagen en la fila 1 columna 0

                self.text = Text(self.subVentana, width=40, height=12) # creamos un campo de texto para insertar la informacion respectiva al estado de salud del coral
                self.text.insert(tkinter.END, 'El coral tiene una anomalia en su estructura') # Texto informativo
                self.text.grid(row = 1, column = 1) # se posiciona a la derecha de la imagen en la fila 1 columna 1

                # Mientras esto sucede, se crea inmediatamente un boton en la ventana principal 
                # para realizar una nueva prediccion y tambien se crea un boton en la misma ventana principal para salir
                self.botonNvaDeteccion = Button(self.master, text="Nueva Detección", command=self.Limpiar) # al momento de realizar una nueva prediccion, los botones se eliminan y se limpia la pantalla dejando unicamente el boton para seleccionar la imagen a evaluar
                self.botonNvaDeteccion.pack()
                self.botonSalir = Button(self.master, text="Salir", command=self.Salir) # boton para salir
                self.botonSalir.pack()

        elif respuesta == 1: # Se definen los mismos pasos cuando la prediccion es 1 == SANO
            print(respuesta)
            self.subVentana = Toplevel()
            self.subVentana.geometry("600x300+300+150")
            self.subVentana.wm_title("(Tesis)Información de Sobre Estado de Salud")
            self.subVentana.focus_set()
            self.subVentana.grab_set()
            self.pred = Label(self.subVentana, text = "Coral SANO detectado")
            self.pred.grid(row = 0, column = 0)
            self.pred.config(fg = "black", font = ("verdana", 12))
            
            # de igual manera se definen las mismas funcionalidades para cuando es un coral sano
            if panel_ventana_prediccion == None:
                self.panel_ventana_prediccion = Label(self.subVentana, image = self.imagen_configurada)
                self.panel_ventana_prediccion.grid(row = 1, column = 0)

                self.text = Text(self.subVentana, width = 40, height = 12)
                self.text.insert(tkinter.END, 'El coral tiene una estructura normal sin niguna alteracion')
                self.text.grid(row = 1, column = 1)

                self.botonNvaDeteccion = Button(self.master, text="Nueva Detección", command=self.Limpiar)
                self.botonNvaDeteccion.pack()
                self.botonSalir = Button(self.master, text ="Salir", command=self.Salir)
                self.botonSalir.pack()

        def CerrarVentanaSecundaria(): # funcion local(pertenece a predict()) para cerrar la ventana secundaria
            self.subVentana.quit() 
            self.subVentana.destroy() 
                                
        buttonCerrar = Button(self.subVentana, text="Cerrar", command=CerrarVentanaSecundaria) # Se crea el boton que aparecera en la ventana secuendaria para salir
        buttonCerrar.grid(row = 2, column = 3) # este ira en la fila 2 y columna 3
        self.master.wait_window(self.subVentana) # espera hasta que la subventana sea destruida

        return respuesta # Retorna el valor 0 o 1 dependiendo de la prediccion

    # Este metodo sirve para eliminar los widgets una vez realizada una nueva prediccion, y agregar los widgets para una nueva deteccion
    def Limpiar(self):
        super().eliminar_widgets(self.botonNvaDeteccion, self.botonSalir)
        super().insertar_widgets(self.etiqueta_imagen, self.boton_cargar_imagen, self.panelLogo)

    # Esta metodo sirve para cerrar LA VENTANA PRINCIPAL   
    def Salir(self):
        self.master.destroy()
        
# METODO MAIN PARA HACER FUNCIONAR LA UI
if __name__ == "__main__":
    root = Tk() # creamos una instancia de tkinter
    Principal(root) # se la pasamos a nuestra clase para que sea ejecutado