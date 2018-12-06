#! /usr/bin/env python
#-*- coding: UTF-8 -*-
import pygame
from herramientas import *
from locales import *
from exceptions import *

'''Módulo con los controles más comunes en la implementación de una interfaz gráfica.'''

class Control(pygame.Surface):
    """Clase base de la cual derivan todos los controles. En ésta clase están definidas las propiedades y métodos que
    tienen en común todos los controles. Algunas propiedades y/o métodos definidos aquí deben ser extendidos o 
    redefinidos en la definición propia del control para su correcto funcionamiento.

    El constructor de ésta clase recibe 2 argumentos obligatorios. El primero es un objeto pygame.Rect o una tupla de 4
    enteros que definen la posicion y el tamaño del control. El segundo es un string conteniendo un nombre para el
    control, que debe ser único entre todos los controles."""

    # Propiedades de clase
    _controls = {}


    # Metodos estaticos
    @staticmethod
    def controls(name):
        '''Devuelve el control con nombre name, de entre todos los controles creados'''
        return _controls[name]



    def __init__(self, rect, name):

        super(Control, self).__init__((rect[2], rect[3]), pygame.HWSURFACE|pygame.SRCALPHA)

        if name in Control._controls:
            raise controlExistente(name)

        self._name = name
        self._pos = (rect[0], rect[1])
        self._size = (rect[2], rect[3])
        self._border = Border()
        self._visible = True
        self._enable = True
        self._focusable = True
        self._screen = Screen()
        self._background = Layer()
        self._foreground = Layer()
        self._font = Font.Default
        self._tag = None
        self._focusOrder = 0

        


    @property
    def name(self):
        '''Nombre del control. Solo lectura'''
        return self._name

    @property
    def pos(self):
        '''Posicion del control'''
        return self.pos
        
    @pos.setter
    def pos(self, val):
        self._nombre = val
    
    @property
    def size(self):
        '''Tamaño del control. Solo lectura'''
        return self._size

    @property
    def border(self):
        '''Objeto de tipo Border() para definir el borde del control'''
        return self._border
        
    @border.setter
    def border(self, val):
        self._border = val

    @property
    def visible(self):
        '''Indica si el control se debe dibujar o no'''
        return self._visible
        
    @visible.setter
    def visible(self, val):
        self._visible = val
    
    
    @property
    def enable(self):
        '''Indica si el control puede interactuar con el usuario'''
        return self._enable
        
    @enable.setter
    def enable(self, val):
        self._enable = val
    

    @property
    def focusable(self):
        '''Indica si el control puede obtener el foco'''
        return self._focusable
        
    @focusable.setter
    def focusable(self, val):
        self._focusable = val
    
    
    @property
    def screen(self):
        '''Pantalla a la que pertenece el control.'''
        return self._screen
        
    @screen.setter
    def screen(self, val):
        self._screen.removeControl(self)  # Elimino el control de la pantalla a la que pertenece actualmente
        val.addControl(self) # Agrego el control a la pantalla nueva
        self._screen = val  # Indico en _screen que esta va a ser la pantalla del control
    
    @property
    def background(self):
        '''Capa de fondo del control'''
        return self._background
        
    @background.setter
    def background(self, val):
        self._background = val
    
    @property
    def foreground(self):
        '''Capa frontal del control'''
        return self._foreground
        
    @foreground.setter
    def foreground(self, val):
        self._foreground = val
    
    @property
    def font(self):
        '''Fuente a usar con el texto del control'''
        return self._font
        
    @font.setter
    def font(self, val):
        self._font = val
    
    @property
    def tag(self):
        '''Propiedad utilizada para guardar cualquier tipo de dato'''
        return self._tag
        
    @tag.setter
    def tag(self, val):
        self._tag = val
    
    @property
    def focusOrder(self):
        '''Entero con el orden de obtención del foco. No pueden haber dos números iguales en una misma pantalla, de ser
        así esta propiedad se modificará automáticamente al agregarla a la pantalla asignada'''
        return self._focusOrder
        
    @focusOrder.setter
    def focusOrder(self, val):
        self._focusOrder = val
    
                                        
   

    def is_hover():
        '''Devuelve un entero indicando si el mouse está sobre el control. Si el resultado es 0 el mouse se encuentra
        fuera del control, si es distinto de 0 está sobre el control.'''
        pass

    def is_down():
        '''Devuelve un entero indicando si algún botón del mouse está presionado sobre el control. Si el resultado es 0
        no hay ningún botón presionado. De ser distinto de 0, el número obtenido indica que botón hay presionado'''
        pass

    def is_focus():
        '''Devuelve True si el foco está situado sobre el control, de lo contrario devuelve False'''
        pass

    def update():
        '''Actualiza los gráficos del control. Debe llamarse a este método cuando cambia alguna propiedad relacionada a 
        los gráficos'''
        pass

    def render(dislay):
        '''Dibuja el control en el display pasado'''
        pass




        