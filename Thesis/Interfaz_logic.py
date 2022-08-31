# en esta clase se definen los metodos con la respectiva logica que se utilizaran en la interfaz

import cv2
import Interfaz
from PIL import Image, ImageTk
from tkinter import *
from tkinter import filedialog as fd 
from tkinter import Tk, Label, Button, Entry, ttk

def configurar_img(self, ubicacion): ##############
        self.ubicacion = ubicacion
        self.imagen = cv2.imread(self.ubicacion) # Leemos el imagen del ITM
        if (self.imagen.shape[0] and self.imagen.shape[1]) == (108 and 468):
            self.imagen = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2RGB) # Se convierte a RGB
            self.imagen = Image.fromarray(self.imagen) # se convierte de matriz a imagen
            self.imagen = ImageTk.PhotoImage(self.imagen) # se convierte a una PhotoImage para colocar en una etiqueta
        elif (self.imagen.shape[0] and self.imagen.shape[1]) != (108 and 468):
            self.imagen = cv2.resize(self.imagen, (200, 200)) # Se cambia el tamaño a 300x300
            self.imagen = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2RGB) # Se convierte a RGB
            self.imagen = Image.fromarray(self.imagen) # se convierte de matriz a imagen
            self.imagen = ImageTk.PhotoImage(self.imagen) # La funcion PhotoImage() crea una instancia de imagen para colocar en una label
        return self.imagen