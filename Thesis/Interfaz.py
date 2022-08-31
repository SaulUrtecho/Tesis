# ********* PARTE 3: Interfaz grafica UI para validar el modelo *********
# se utiliza la libreria tkinter

from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog as fd  # Esta libreria sirve para abrir una ventana de dialogo
import cv2
from keras_preprocessing import image
import numpy as np
import tensorflow as tf
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
from keras.initializers import glorot_uniform
from tkinter import Tk, Label, Button, Entry, ttk
import tkinter
import re

# Configuramos el alto y ancho que tendran las imagenes a utilizar en la interfaz
longitud, altura = 200, 200
# Definimos las rutas de los archivos necesarios para que funcione el programa
ruta_logo_itm = 'C:/Users/saulu/Documents/SistemaTesis/Thesis/logo.jpg'
ruta_modelo_default = 'C:/Users/saulu/Documents/SistemaTesis/Thesis/DATOS_RED/Modelo.h5'
ruta_pesos_default = 'C:/Users/saulu/Documents/SistemaTesis/Thesis/DATOS_RED/Pesos.h5'

# Esta es la clase que crea la interfaz grafica se utiliza POO
class Principal():
    # Metodo constructor el cual recibe un objeto Tk()
    # este metodo inicializa toda la interfaz
    def __init__(self, master):
        self.master = master
        self.master.title("(TESIS) Predicción de Salud en Corales del Caribe Mexicano")
        self.master.geometry("500x400+450+100")
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
        self.boton_cargar_imagen = Button(self.master, text="Cargar Imagen", command=self.seleccionar_imagen) # Cargar la imagen
        self.boton_cargar_imagen.pack()
        self.var_img = self.configurar_img(ruta_logo_itm)
        self.panelLogo = Label(self.master, image=self.var_img) # El logo se coloca en una etiqueta_imagen
        self.panelLogo.pack(side="bottom")
        self.master.mainloop()  # Este mainloop es el que mantiene la VENTANA PRINCIPAL FUNCIONANDO

    def configurar_img(self, ubicacion): ##############
        self.ubicacion = ubicacion
        self.logo = cv2.imread(self.ubicacion) # Leemos el logo del ITM
        if (self.logo.shape[0] and self.logo.shape[1]) == (108 and 468):
            self.logo = cv2.cvtColor(self.logo, cv2.COLOR_BGR2RGB) # Se convierte a RGB
            self.logo = Image.fromarray(self.logo) # se convierte de matriz a imagen
            self.logo = ImageTk.PhotoImage(self.logo) # se convierte a una PhotoImage para colocar en una etiqueta
        elif (self.logo.shape[0] and self.logo.shape[1]) != (108 and 468):
            self.logo = cv2.resize(self.logo, (longitud, altura)) # Se cambia el tamaño a 300x300
            self.logo = cv2.cvtColor(self.logo, cv2.COLOR_BGR2RGB) # Se convierte a RGB
            self.logo = Image.fromarray(self.logo) # se convierte de matriz a imagen
            self.logo = ImageTk.PhotoImage(self.logo) # La funcion PhotoImage() crea una instancia de imagen para colocar en una label
        return self.logo

    def cargar_modelo(self): # en esta funcion obtenemos la ruta del modelo
        self.ruta_modelo_user = self.abrir_ventana()  # abre cuadro de dialogo para pedir la ruta del modelo al usuario
        if len(self.ruta_modelo_user) > 0:  # si el tamaño de la cadena es mayor a 0, es que existe la ruta
            # si la ruta del usuario es diferente a la ruta por defecto se lanza una ventana de error
            if self.ruta_modelo_user != ruta_modelo_default: 
                self.ventana_alerta()
            else:
                self.eliminar_widgets(self.etiqueta_modelo, self.boton_cargar_modelo)
        return self.ruta_modelo_user  # devolvemos la ruta dada por el usuario
    
    def cargar_pesos(self): # en esta funcion obtenemos la ruta de los pesos
        self.ruta_pesos_user = self.abrir_ventana()
        if len(self.ruta_pesos_user) > 0: # si la ruta del usuario existe
            if self.ruta_pesos_user != ruta_pesos_default:
                self.ventana_alerta()
            else:
                self.eliminar_widgets(self.etiqueta_pesos, self.boton_cargar_pesos)
        return self.ruta_pesos_user

    def eliminar_widgets(self, *args): #######################################
        for arg in range(len(args)):
            self.widgets_borrados = args[arg].pack_forget()
        return self.widgets_borrados 

    def abrir_ventana(self): ###################################################
        self.ruta = fd.askopenfilename()
        return self.ruta
    
    def ventana_alerta(self): ######################################################
        def cerrar_ventana_warning(): 
            self.ventana_aviso.destroy()
        self.ventana_aviso = Toplevel()
        self.ventana_aviso.geometry("300x100+500+250") # Se establece el tamaño de la ventana secundaria
        self.ventana_aviso.wm_title("WARNING!!!") # Se le asigna el titulo
        self.ventana_aviso.focus_set() # Este metodo enfoca la ventana secundaria 
        self.ventana_aviso.grab_set() # desactivamos la ventana principal 
        self.aviso = Label(self.ventana_aviso, text="No ha seleccionado el archivo correcto\nIntente Nuevamente!!") # asignamos la etiqueta_imagen para mencionar que es un coral enfermo
        self.aviso.pack()
        self.aviso.config(fg="black")
        self.botonCerrar = Button(self.ventana_aviso, text='Aceptar', command=cerrar_ventana_warning)
        self.botonCerrar.pack()
        
        
    def seleccionar_imagen(self):
        panel_img_principal = None # esta variable contendra la imagen que se muestra al momento de seleccionar la imagen
        self.ruta_imagen_user = fd.askopenfilename() # Abre una ventana de dialogo para seleccionar una imagen, y devuelve la ruta de la imagen seleccionada
        if len(self.ruta_imagen_user) > 0:
            if re.search("\.(jpg|jpeg|JPG|png|bmp|tiff)$", self.ruta_imagen_user): # Validamos que el usuario haya seleccionado una imagen
                self.eliminar_widgets(self.etiqueta_imagen, self.boton_cargar_imagen, self.panelLogo)
                self.imagen_configurada = self.configurar_img(self.ruta_imagen_user) # se crea una copia de la imagen para colocarla en la ventana secundaria al momento de predecir
                self.botonPredict = Button(text="Detectar Estado de Salud", command=self.prediccion) # se crea el boton que hace la prediccion
                self.botonPredict.pack() # el boton es colocado en la interfaz
                self.boton_selec_otra_img = Button(text="Seleccionar otra imagen", command=self.abrir_otra_img) # se crea un boton debajo por si quiere seleccionar otra imagen
                self.boton_selec_otra_img.pack()

                if panel_img_principal is None: # Si la variable panel_img_principal esta inicializada en nula
                    self.panel_img_principal = Label(self.master, image=self.imagen_configurada)  # se carga la imagen en la label
                    self.panel_img_principal.pack(side="bottom")  
            else:
                self.ventana_alerta()
            self.master.mainloop() # Este mainloop se coloca aqui para mantener la VENTANA PRINCIPAL FUNCIONANDO despues de cerrar la ventana secundaria del resultado de la prediccion

    def abrir_otra_img(self): #############################
        self.eliminar_widgets(self.panel_img_principal, self.botonPredict, self.boton_selec_otra_img)
        self.seleccionar_imagen()


    def prediccion(self):  # esta funcion se activa al momento de darle click al boton "Detectar estado de salud"
        self.eliminar_widgets(self.botonPredict, self.boton_selec_otra_img, self.panel_img_principal)
        
        with tf.keras.utils.custom_object_scope({'GlorotUniform':glorot_uniform()}): # cargamos el modelo y los pesos obtenidos de las rutas
            cnn = load_model(self.ruta_modelo_user)
        cnn.load_weights(self.ruta_pesos_user)

        # Aqui se hace la prediccion obteniendo la imagen de la ruta y cambiandole su tamaño al tamaño que se uso en el entrenamiento 200x200
        x = load_img(self.ruta_imagen_user, target_size = (longitud, altura)) 
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

        # Se definen los mismos pasos cuando la prediccion es 1 == SANO
        elif respuesta == 1:
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
                                
        # Se crea el boton que aparecera en la ventana secuendaria para salir
        buttonCerrar = Button(self.subVentana, text="Cerrar", command=CerrarVentanaSecundaria)
        buttonCerrar.grid(row = 2, column = 3) # este ira en la fila 2 y columna 3

        self.master.wait_window(self.subVentana) # espera hasta que la subventana sea destruida
        return respuesta # Retorna el valor 0 o 1 dependiendo de la prediccion

    # esta funcion sirve para eliminar los widgets una vez realizada una nueva prediccion y agregar los widgets para una nueva deteccion
    def Limpiar(self):  ###############
        self.eliminar_widgets(self.botonNvaDeteccion, self.botonSalir)
        self.etiqueta_imagen.pack()
        self.boton_cargar_imagen.pack()
        self.panelLogo.pack(side = "bottom")

    # esta funcion sirve para cerrar LA VENTANA PRINCIPAL   
    def Salir(self): ###############
        self.master.destroy()
        
      
# METODO MAIN PARA HACER FUNCIONAR LA UI
if __name__ == "__main__":
    root = Tk()
    Principal(root)
  