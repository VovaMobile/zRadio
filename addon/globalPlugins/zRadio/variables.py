# -*- coding: utf-8 -*-
# Copyright (C) 2020 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import sys
import os
from .pathlib import Path
import pickle
import ctypes
import globalVars
import addonHandler
from .reproductor import *

# For translation
addonHandler.initTranslation()

dir = addonHandler._getDefaultAddonPaths()
dirDatos =os.path.join(globalVars.appArgs.configPath, "zRadio")
dirLib =os.path.join(dir[0], "zRadio", "globalPlugins","zRadio", "lib")
fileOptions = os.path.join(dirDatos, "opciones.dat")
fileOptionsRadio = os.path.join(dirDatos, "opt_radio.dat")
fileFavRadio = os.path.join(dirDatos, "fav_radios.dat")

class Guardar_Cargar():
	def __init__(self):

		self.version = 1
		self.volumen = 50

		self.fav_nombre_radios = []
		self.fav_url_radios = []

		self.PestañaGeneralRadioOpciones = ["", ""]

	def Guardar_Opciones(self, lista):
		archivo = open(	fileOptions, "wb")
		pickle.dump(self.version, archivo)
		for i in lista:
			pickle.dump(i, archivo)
		archivo.close()

	def Cargar_Opciones(self):
		if os.path.isfile(fileOptions):
			archivo = open(	fileOptions, 'rb')
			self.version = pickle.load(archivo)
			if self.version == 1:	
				self.volumen = pickle.load(archivo)
			archivo.close()
		else:
			lista_opciones = [self.volumen]
			Guardar_Cargar.Guardar_Opciones(self, lista_opciones)
			Guardar_Cargar.Cargar_Opciones(self)

	def Guardar_Opciones_Radio(self, lista):
		archivo = open(	fileOptionsRadio, "wb")
		pickle.dump(self.version, archivo)
		for i in lista:
			pickle.dump(i, archivo)
		archivo.close()

	def Cargar_Opciones_Radio(self):
		if os.path.isfile(fileOptionsRadio):
			archivo = open(	fileOptionsRadio, 'rb')
			self.version = pickle.load(archivo)
			if self.version == 1:	
				self.PestañaGeneralRadioOpciones = pickle.load(archivo)
			archivo.close()
		else:
			lista_opciones = [self.PestañaGeneralRadioOpciones]
			Guardar_Cargar.Guardar_Opciones_Radio(self, lista_opciones)
			Guardar_Cargar.Cargar_Opciones_Radio(self)

	def Guardar_Buffers(self, file,  *args):
		archivo = open(file, "wb")
		for i in args:
			pickle.dump(i, archivo)
		archivo.close()

	def Cargar_Buffer_Favoritos_Radio(self):
		if os.path.isfile(fileFavRadio):
			archivo = open(fileFavRadio, 'rb')
			self.fav_nombre_radios = pickle.load(archivo)
			self.fav_url_radios = pickle.load(archivo)
			archivo.close()
		else:
			Guardar_Cargar.Guardar_Buffers(self, fileFavRadio, self.fav_nombre_radios, self.fav_url_radios)

### Variables Raspado
if os.path.isfile(os.path.join(dirDatos, "cache.dat")):
	os.remove(os.path.join(dirDatos, "cache.dat"))
if os.path.isfile(os.path.join(dirDatos, "radio_cache.dat")):
	os.remove(os.path.join(dirDatos, "radio_cache.dat"))
if os.path.isdir(dirDatos):
	pass
else:
	os.mkdir(dirDatos)

Opciones = Guardar_Cargar()
Radios = None
player = MPVClass()
### Listas
listaCategoriasBusquedaRadios = [
	# Translators: Options for the search category combobox
	_("Búsqueda general de radios"),
	# Translators: Options for the search category combobox
	_("Búsqueda por países"),
	# Translators: Options for the search category combobox
	_("Búsqueda por idioma"),
	# Translators: Options for the search category combobox
	_("Búsqueda por etiqueta")]

### Variables generales
nombreTitulo = "" # Adquiere el titulo de la ventana para cuando se reproduce
urlReproducir = "" # La dirección a reproducir

### Controles
control1 = False
controlON = False
controlSilenciar = False
controleditor = False

PestañaGeneralRadioOpciones = None
gen_nombre_radios = []
gen_url_radios = []
fav_nombre_radios = []
fav_url_radios = []
temporal_nombre_radio_favoritos = []
temporal_url_radio_favoritos = []
# Translators: Message without stations
nombre_emisoras_temporal = [_("Sin emisoras.")]
url_emisoras_temporal = []
nombre_emisoras_temporal_busqueda = []
url_emisoras_temporal_busqueda = []

### Variantes configuración
Opciones.Cargar_Opciones()
volumenGeneral = int(Opciones.volumen)

