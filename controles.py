#! /usr/bin/env python
#-*- coding: UTF-8 -*-
import pygame
from herramientas import *
from locales import *
from exceptions import *

'''Módulo con los controles más comunes en la implementación de una interfaz gráfica.'''

class Screen(object):
    """Clase que agrupa un conjunto de controles que define una pantalla. Recibe solo un parámetro, que es un string
    con el nombre de la pantalla, que debe ser único entre todas las pantallas."""

    _screens = {}
    _current = None
    _prev = None


    @staticmethod
    def set_current(name):
        '''Cambia la pantalla actual por la indicada en name'''
        pass

    @staticmethod
    def set_prev():
        '''Cambia la pantalla actual por la anterior'''
        pass

    @staticmethod
    def screens():
        '''Devuelve una lista con las pantallas disponibles'''
        return Screen._screens.values()

    

    def __init__(self, name):

        # Propiedades principales: nombre y controles
        self._name = name
        self._controls = {}

        # Establezco el fondo y sus caracteristicas
        self._background_type = T_DRAW
        self._background_color = Color.Black
        self._background_image = None


        # Establezco el foco y sus caracteristicas
        self._focus = None
        self._focus_border = Border()

        self._focus_border.color = Color.Red
        self._focus_border.size = 1
        self._focus_border.style = S_SOLID
        self._focus_border.show = True
        

        # Agrego la pantalla al diccionario. Si ya existe lanzo una excepcion
        if name in Screen._screens:
            raise screenExistente(name)

        Screen._screens[name] = self






    # FUNCIONES PARA EL MANEJO DE CONTROLES


    def addControl(self, control):
        '''Agrega el control pasado a la lista de controles de la pantalla'''

        # Agrega el control solo si no existe en el diccionario
        if control.name in self._controls:  
            raise controlExistente(control.name)

        self._controls[control.name] = control
        control._Controls__screen = self

        # Verifica que el orden del foco en el control sea valido
        fo = [n for self.get_controls().focusOrder]  # Lista de focusOrder usados

        if control.focusOrder in fo: # Si el orden del control ya existe ...
            n = 1
            while n in fo:           # ... Busco un orden nuevo que sea valido ...
                n += 1

            control.focusOrder = n   # ... y se lo asigno al control




    def removeControl(self, name):
        '''Quita el control de nombre name de la lista de controles de la pantalla y devuelve el control quitado'''

        if name in self._controls:
            c = self._controls.pop(name)
            c._Controls__screen = None
            return c
        else:
            raise controlInexistente(name)


    def get_controls(self):
        '''Devuelve una lista con los controles de la pantalla'''
        return self._controls.values()


    def get_control(self, name, raiseErr=True):
        '''Devuelve el control indicado en name. Si no existe y raiseErr=True lanza una excepcion, de lo contrario devuelve None'''

        if name in self._controls:
            return self._controls[name]
        else:
            if raiseErr:
                raise controlInexistente
            else:
                return None



    # FUNCIONES PARA EL MANEJO DEL FOCO

    
    def set_focus(self, control):
        '''Pongo el foco en el control pasado'''
        self._focus = control

    def focus_next(self):
        '''Pasa el foco al siguiente control de la lista, o al siguiente elemento del control si lo tuviera.'''

        
        if self._focus != None:
            if self._focus.change_focus(D_NEXT):
                lo = self.get_controls().sort(key=lambda ctrl: ctrl.focusOrder) # Lista ordenada
                fin = True # Variable auxiliar que me sirve para saber si llegue al final de la lista
            
                for c in lo:
                    if c.focusOrder > self._focus.focusOrder:  # Si durante el bucle el focusOrder es mayor que el actual...
                        self._focus = c                        # ... asigno el encontrado como actual ...
                        fin = False                            # ... cambio la bandera a False para indicar que no llegué hasta el final...
                        break                                  # ... y salgo del bucle


                if fin:                       # Si en el bucle había llegado hasta el final, es xq el focusOrder actual era el mas alto ...
                    self._focus = lo[0]       # ... y por lo tanto salió del bucle normalmente. En este caso asigno el primer control.





    def focus_prev(self):
        '''Pasa el foco al control anterior de la lista, o al elemento anterior del control si lo tuviera.'''

        if self._focus != None:
            if self._focus.change_focus(D_PREV):
                lo = self.get_controls().sort(reverse=True, key=lambda ctrl: ctrl.focusOrder) # Lista ordenada en reversa
                fin = True # Variable auxiliar que me sirve para saber si llegue al final de la lista
            
                for c in lo:
                    if c.focusOrder < self._focus.focusOrder:  # Si durante el bucle el focusOrder es menor que el actual...
                        self._focus = c                        # ... asigno el encontrado como actual ...
                        fin = False                            # ... cambio la bandera a False para indicar que no llegué hasta el final...
                        break                                  # ... y salgo del bucle


                if fin:                       # Si en el bucle había llegado hasta el final, es xq el focusOrder actual era el mas bajo ...
                    self._focus = lo[0]       # ... y por lo tanto salió del bucle normalmente. En este caso asigno el primer control ...
                                              # ... ya que al estar ordenada en reversa el primer elemento de la lista es el mayor



    # FUNCIONES DE DIBUJADO

    def render(self, display):
        '''Dibuja todos los controles de la pantalla en el display pasado'''

        for ctl in self.get_controls():
            ctl.render(display)


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
        self._screen = None    #  Inicialmente no tiene pantalla
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
        '''Pantalla a la que pertenece el control. Solo lectura'''
        return self._screen
      

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
        '''Entero mayor o igual que 0 con el orden de obtención del foco. No pueden haber dos números iguales en una 
        misma pantalla, de ser así esta propiedad se modificará automáticamente al agregarla a la pantalla asignada.'''
        return self._focusOrder
        
    @focusOrder.setter
    def focusOrder(self, val):
        if val < 0: 
            val = 0
        self._focusOrder = val
    
                                        
   
    # VERIFICACIONES

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

    def change_focus(self, dir=None):
        '''Verifica si el control puede soltar el foco. Si dir=None solo es una consulta y devuelve un valor de 
        dirección. Si se especifica una dirección devuelve True o False según corresponda, y en caso de tener elementos
        propios actúa en consecuencia.''' 
        
        # Este metodo debe extenderse cuando el control tiene elementos que pueden obtener el foco
        if dir == None:
            return D_PREVNEXT
        else:
            return True

    
    # METODOS Y FUNCIONES PARA EXTENDER EN LAS CLASES DERIVADAS

    def update():
        '''Actualiza los gráficos del control. Debe llamarse a este método cuando cambia alguna propiedad relacionada a 
        los gráficos'''
        pass

    def render(dislay):
        '''Dibuja el control en el display pasado'''
        pass


    # METODOS Y FUNCIONES PARA MANEJO DE LA PANTALLA DEL CONTROL

    def drop_screen(self):
        '''Desvincula el control de cualquier pantalla'''
        if self._screen != None:
            self._screen.removeControl(self.name) # Este método del objeto Screen automáticamente coloca None en _screen

    def get_screen(self):
        '''Obtiene la pantalla del control. Es el mismo resultado que la propiedad screen'''
        return self.screen

    def set_screen(self, pantalla):
        '''Asigna el control a la pantalla pasada'''

        # Solo se puede asignar a una pantalla cuando no pertenece a ninguna. Si ya es parte de una pantalla debe
        # dejarla antes de pertenecer a otra. Cada control solo puede formar parte de una pantalla
        if self._screen == None:
            pantalla.addControl(self) # Este método del objeto Screen asigna automáticamente la pantalla a _screen

        else:
            raise screenAsignada(self.name)


        