# In this class we will define some methods which it contains its logic than will to inherit to main GUI

import cv2
from PIL import ImageTk
from PIL import Image as Img
from tkinter import Toplevel
from tkinter import filedialog as fd 
from tkinter import Label, Button

class tools():
    # Method than provide the image configuration
    def configurar_img(self, ubicacion): 
            self.ubicacion = ubicacion
            self.imagen = cv2.imread(self.ubicacion) # we read the image 
            if (self.imagen.shape[0] and self.imagen.shape[1]) == (108 and 468): # if the image is the same size of the logo.jpg size, then it stays 
                self.imagen = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2RGB) # image will convert to RGB
                self.imagen = Img.fromarray(self.imagen) # it is convert from matrix to image
                self.imagen = ImageTk.PhotoImage(self.imagen) # it is convert to PhotoImage to set in a label
            elif (self.imagen.shape[0] and self.imagen.shape[1]) != (108 and 468): # if the image is any other size different to logo.jpg
                self.imagen = cv2.resize(self.imagen, (200, 200)) # we change the size to 200x200
                self.imagen = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2RGB)
                self.imagen = Img.fromarray(self.imagen)
                self.imagen = ImageTk.PhotoImage(self.imagen)
            return self.imagen # return the configured image
    
    # Method for erase n quantity of widgets than aren't necessary
    def eliminar_widgets(self, *args):
        for arg in range(len(args)):
            self.widgets_borrados = args[arg].pack_forget()
        return self.widgets_borrados 

    # Method for insert n quantity of widgets on GUI
    def insertar_widgets(self, *args): 
        for item in range(len(args)):
            if args[item] == self.panelLogo: # if the widget is equals to self.panel then it going to GUI bottom 
                args[item].pack(side = "bottom")
            else:
                args[item].pack()

    # Method for open a window file dialog
    def abrir_ventana(self):
            self.ruta = fd.askopenfilename()
            return self.ruta # return the file path

    # Method for throw a window alert if the user select a wrong file
    def ventana_alerta(self):
        def cerrar_ventana_warning(): # local function for destroy window alert
            self.ventana_aviso.destroy()
        self.ventana_aviso = Toplevel()
        self.ventana_aviso.geometry("300x100+500+250") # set the size 
        self.ventana_aviso.wm_title("WARNING!!!") # set the title
        self.ventana_aviso.focus_set() # focus the secondary window
        self.ventana_aviso.grab_set() # we desactivate the main window
        self.aviso = Label(self.ventana_aviso, text="No ha seleccionado el archivo correcto\nIntente Nuevamente!!") # we set a information text for advice to user than something did wrong
        self.aviso.pack()
        self.aviso.config(fg="black")
        self.botonCerrar = Button(self.ventana_aviso, text='Aceptar', command=cerrar_ventana_warning)
        self.botonCerrar.pack()