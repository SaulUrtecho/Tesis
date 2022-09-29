'''
Script para comprobar el funcionamiento de una matriz numpy y el acceso a sus posiciones
esta comprobacion me sirvio al momento de crear el excel y la matriz de confusion en el modulo
Confusion_Matrix.py

import numpy as np
from keras.preprocessing.image import load_img, img_to_array
from PIL import Image, ImageTk

arreglo = [[1,9],[2,8],[3,7],[4,5],[5,4],[7,3],[8,2],[9,1]]

listaNumpy = np.array(arreglo) # convertimos la lista en un arreglo numpy

print(listaNumpy[:,1])  # modificando el segundo parametro podemos acceder a las posiciones de cada subvector de la matriz

'''

'''
** script para ver la forma y tipo de una imagen especifica **

longitud = 200
altura = 200

x = load_img('./sano.jpg', target_size = (longitud, altura))
x = img_to_array(x)
print(x.shape)
print(type(x))
x = np.expand_dims(x, axis = 0)
print(x.shape)
print(type(x))

'''

'''

Esta clase me sirvio para comprobar la ruta que se obtiene de un filedialog

from tkinter import*
from tkinter import filedialog as fd 
from tkinter import Tk, Label, Button, Entry, ttk
import tkinter
from os import path
class BotonPrueba():

    def __init__(self, master):
        self.master = master
        self.master.geometry("300x200+450+100")
        self.botonCargarModelo = Button(self.master, text="Cargar Modelo", command=self.cargar_modelo) # boton para cargar el modelo obtenido de la red
        self.botonCargarModelo.pack()
        self.botonSalir = Button(self.master,text="salir",command=self.Salir)
        self.botonSalir.pack()
        self.master.mainloop()

    def cargar_modelo(self):
        self.ruta_modelo = fd.askopenfilename()
        print(self.ruta_modelo)
        self.ruta_modelo = path.split(self.ruta_modelo)
        print(self.ruta_modelo)
        

    def Salir(self):
        self.master.destroy()



if __name__ == "__main__":
    root = Tk()
    BotonPrueba(root)

'''

'''
Este script me sirvio para acceder al alto y ancho de una imagen

import cv2
 
# read image
img = cv2.imread('C:/Users/saulu/Documents/SistemaTesis/Thesis/logo.jpg', cv2.IMREAD_UNCHANGED)
 
# get dimensions of image
dimensions = img.shape
 
# height, width, number of channels in image
height = img.shape[0]
width = img.shape[1]
 
print('Image Height       : ',height)
print('Image Width        : ',width)
print(type(height))

'''

'''

#ESTE SCRIPT ME SIRVIO PARA USAR EL FILTRO MEDIANO

from PIL import Image, ImageEnhance, ImageFilter
import re 
import os

#imgpath = 'C:/Users/saulm/Documents/Python/Deep_Learning/RNC/Coral_Reef_Disease/test_set'
imgpath = 'C:/Users/saulu/Documents/SistemaTesis/Thesis/DATASET/TRAINING_SET'
images = []
dircount = []
cant = 0

print("leyendo imagenes de: ", imgpath)
for root, dirnames, filenames in os.walk(imgpath):
    for filename in filenames:
        if re.search("\.(jpg|jpeg|JPG|png|bmp|tiff)$", filename):
            filepath = os.path.join(root, filename)
            imagen = Image.open(filepath)
            #convirtiendo a RBG
            imagen = imagen.convert("RGB")
            img_modify = imagen.filter(ImageFilter.MedianFilter(size=5))
            img_modify.save('./train_set_median/' + str(cant) + ".jpg")
            cant = cant + 1
            b = "Leyendo..." + str(cant)
            print(b,end="\r")
           
dircount.append(cant)
print("Imagenes en cada directorio", dircount)
print("suma total de imagenes en subdirs", sum(dircount))

'''

'''

#ESTE SCRIPT ME SIRVIO PARA ROTAR LAS IMAGENES Y ASI AUMENTAR EL DATASET

from PIL import Image
import os
import glob
import re

#print(os.getcwd())

dirname = os.path.join(os.getcwd(), './healthy')    # se une la ruta actual con la ruta de las imagenes
imgpath = dirname + os.sep      # se obtiene la ruta definitiva 

images = []
dircount = []
cant = 0

print("leyendo imagenes de: ", imgpath)

for root, dirnames, filenames in os.walk(imgpath):
    for filename in filenames:
        if re.search("\.(jpg|jpeg|JPG|png|bmp|tiff)$", filename):
            filepath = os.path.join(root, filename)
            imagen = Image.open(filepath)
            imagen_rotada90 = imagen.rotate(90)
            imagen_rotada180 = imagen.rotate(180)
            imagen_rotada270 = imagen.rotate(270)

            #convirtiendo a RBG
            imagen_rotada90 = imagen_rotada90.convert("RGB")
            imagen_rotada180 = imagen_rotada180.convert("RGB")
            imagen_rotada270 = imagen_rotada270.convert("RGB")

            imagen_rotada90.save('./rotadas_san/' + str(cant) + "_90_grados_.jpg")
            imagen_rotada180.save('./rotadas_san/' + str(cant) + "_180_grados_.jpg")
            imagen_rotada270.save('./rotadas_san/' + str(cant) + "_270_grados_.jpg")
            cant = cant + 1

            b = "Leyendo..." + str(cant)
            print(b,end="\r")
           
dircount.append(cant)
print("Imagenes en cada directorio", dircount)
print("suma total de imagenes en subdirs", sum(dircount))

'''