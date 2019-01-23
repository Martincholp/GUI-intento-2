#! /usr/bin/env python
#-*- coding: UTF-8 -*-
import pygame
from controles import *
from herramientas import *
from locales import *
from exceptions import *

'''Módulo con controles avanzados en la implementación de una interfaz gráfica.
Controloes incluidos en este módulo:
  SliderV:   Barra deslizable vertical'''

class SliderV(Control):
    '''Barra deslizable vertical'''
    

    def __init__(self, rect, name):
        super(SliderV,self).__init__(rect, name)
    
    
        self.__max = 100
        self.__min = 0
        self.__value = 50
        self.__orientation = O_VERTICAL


        # Cursor
        self.__cursorThickness = 5
        self.__cursorSize = (rect[2], self.__cursorThickness)
        self.__cursorPos = (0,0)
        self.__cursor = Layer()
        self.__arrastrar = False # variable auxiliar para el arrastrado del cursor

        # Linea central
        self.__centralLine = Line()  #  Grosor de la linea central del control

        self.__setCursorPos()  # Actualiza la posicion del cursor


    @property
    def cursorThickness(self):
        '''Establece el ancho del cursor'''
        return self.__cursorThickness
    
    @cursorThickness.setter
    def cursorThickness(self, v):
        self.__cursorThickness = v

        if self.__orientation == O_HORIZONTAL:
            self.cursorSize = (self.__cursorThickness, self.get_height()) 
        elif self.__orientation == O_VERTICAL:
            self.cursorSize = (self.get_width(), self.__cursorThickness) 


    @property
    def cursorSize(self):
        '''Tupla con el tamaño del cursor.'''
        return self.__cursorSize
    
    @cursorSize.setter
    def cursorSize(self, val):
        self.__cursorSize = val
        self.__cursor.normal_image = pygame.Surface(val, pygame.HWSURFACE|pygame.SRCALPHA)
        self.__cursor.hover_image = pygame.Surface(val, pygame.HWSURFACE|pygame.SRCALPHA)
        self.__cursor.down_image = pygame.Surface(val, pygame.HWSURFACE|pygame.SRCALPHA)
        self.__cursor.disable_image = pygame.Surface(val, pygame.HWSURFACE|pygame.SRCALPHA)
        
        self.__setCursorPos()

    
    @property
    def centralLine(self):
        '''Ancho de la línea central del control'''

        return self.__centralLine


    @centralLine.setter
    def centralLine(self, val):
        self.__centralLine = val

        


    @property
    def orientation(self):
        '''Orientacion del control. Solo lectura'''
        return self.__orientation


    @property
    def cursorPos(self):
        '''Posicion del cursor. Solo lectura'''
        return self.__cursorPos
    
    def __setCursorPos(self):
        '''Setea la posicion del cursor en funcion del valor max, valor min y el valor actual. Es de uso privado'''

        if self.orientation == O_HORIZONTAL:
            self.__cursorPos = ((self.get_width()-self.cursorThickness)*(self.__value-self.__min)/(self.__max-self.__min)+self.left, self.top +(self.get_height()-self.__cursorSize[1])/2 )
        
        elif self.orientation == O_VERTICAL:
            self.__cursorPos = (self.left +(self.get_width()-self.__cursorSize[0])/2, (-1*(self.get_height()-self.cursorThickness)*(self.__value-self.__min)/(self.__max-self.__min)+self.top+self.get_height()-self.cursorThickness )) #-self.height)


    @property
    def maxValue(self):
        '''Valor máximo'''
        return self.__max

    @maxValue.setter
    def maxValue(self, v):
        self.__max = v

        if (self.__max-self.__min):  # Esto es para evitar division por cero
            self.value = self.__value  # Recalcula la posicion actual, por si quedo fuera del nuevo limite

    @property
    def minValue(self):
        '''Valor mínimo'''
        return self.__min

    @minValue.setter
    def minValue(self, v):
        self.__min = v

        if (self.__max-self.__min):  # Esto es para evitar division por cero
            self.value = self.__value  # Recalcula la posicion actual, por si quedo fuera del nuevo limite

    @property
    def value(self):
        '''Valor actual'''
        return self.__value

    @value.setter
    def value(self, v):
        if v < self._min:
            self.__value = self.__min
        elif v > self.__max:
            self.__value = self.__max
        else:            
            self.__value = v
    
        self.__setCursorPos()
        

    def render(self, target, b=None):
        '''Dibuja el control en la superficie indicada en target.'''

        r = super(Slider, self).render(target, b)

        #  Las siguientes instrucciones solo dibujan el cursor en la posicion correspondiente,
        #  el rectangulo del control ya fue dibujado por el render de la clase base

        #  Si no hay presionado ningun boton detiene la operacion de arrastrar si se ha iniciado
        btns = pygame.mouse.get_pressed()
        if not (btns[0] or btns[1] or btns[2]):  
            self.__arrastrar = False

        if r :
            h = self.is_hover()

            if not self.enable:
                target.blit(self.cursor.disable_image, self.cursorPos)
            else:
                if h: 
                    if self.is_down(b):

                        if self.__arrastrar:
                            if self.orientation == O_HORIZONTAL:
                                self.value = ((self.maxValue-self.minValue+1)*(pygame.mouse.get_pos()[0]-self.left)/self.get_width())+self.minValue

                            elif self.orientation == O_VERTICAL:
                                self.value = self.minValue + (pygame.mouse.get_pos()[1]-self.top-self.get_height())*(self.maxValue-self.minValue)/(-1*self.get_height())

                        target.blit(self.cursor.down_image, self.cursorPos)
                    else:
                        target.blit(self.cursor.hover_image, self.cursorPos)
                else:
                    target.blit(self.cursor.normal_image, self.cursorPos)
       




    def update(self):
        '''Actualiza como se mostrará el control según el modo gráfico establecido. Debe ser llamado cada vez que la imagen del control cambie'''



        # Actualizo la posicion del cursor
        self.__setCursorPos()

        # Linea central
        pygame.draw.line(self.normal_image, self.normal_color, (self.get_width()/2, 0), (self.get_width()/2, self.get_height()), self.__centralLine.size) #(0, (self.height-self.centralLineSize)/2, self.width, self.centralLineSize), 1)
        pygame.draw.line(self.hover_image, self.hover_color, (self.get_width()/2, 0), (self.get_width()/2, self.get_height()), self.__centralLine.size) #(0, (self.height-self.centralLineSize)/2, self.width, self.centralLineSize), 1)
        pygame.draw.line(self.down_image, self.down_color, (self.get_width()/2, 0), (self.get_width()/2, self.get_height()), self.__centralLine.size) #(0, (self.height-self.centralLineSize)/2, self.width, self.centralLineSize), 1)
        # Cursor
        pygame.draw.rect(self.__cursor.normal_image, self.__cursor.normal_color, (0,0,self.cursorSize[0], self.cursorSize[1]), 0)
        pygame.draw.rect(self.__cursor.hover_image , self.__cursor.hover_color , (0,0,self.cursorSize[0], self.cursorSize[1]), 0)
        pygame.draw.rect(self.__cursor.down_image, self.__cursor.down_color, (0,0,self.cursorSize[0], self.cursorSize[1]), 0)
    
        


    def is_hover(self):
        '''Devuelve un entero mayor que cero cuando el cursor del mouse está sobre el control.
        Tabla de valores:
            0 --> No está sobre el control
            1 --> Está sobre el cursor del control
            2 --> Está sobre la línea central del control
            3 --> Está sobre el control (pero fuera del cursor y la línea central)'''
        
        pos = pygame.mouse.get_pos()  #  Posicion del mouse
        res = 0  #  Valor por defecto
        
        if self.visible and self.is_context():

                #  Sobre el control
            if self.get_rect().collidepoint(pos):
                res = 3  

                #  Sobre la linea
            if (pos[0] > self.left + self.width / 2 - self.__centralLine.size / 2) and (pos[0] < self.left + self.width / 2 + self.__centralLine.size / 2):    # self._centralLineSize.move(self.left,self.top).collidepoint(pos):
                res = 2

                #  Sobre el cursor
            if self.img_cursorNormal.get_rect(topleft = self.cursorPos).collidepoint(pos):
                res = 1

            return res


    def click(self, boton=None):
        '''Establece el valor del control según donde se hizo click. Si es sobre la línea central
        posiciona el cursor allí y establece el valor. Si es sobre el cursor inicia una operación
        de arrastrar para posicionarlo y establecer el valor'''


        esta_encima = self.is_hover()
        pos = pygame.mouse.get_pos()
                   
        if esta_encima:
            if self.enable:
                if self.enableFocus:
                    ControlBase.OnFocus = self

            if esta_encima == 1:  # sobre el cursor
                self._arrastrar = True

            elif esta_encima == 2:  # Sobre la linea
                if self.orientation == O_HORIZONTAL:
                    self.value = ((self.maxValue-self.minValue+1)*(pos[0]-self.left)/self.width)+self.minValue
                
                elif self.orientation == O_VERTICAL:
                    self.value = self.minValue + (pygame.mouse.get_pos()[1]-self.top-self.height)*(self.maxValue-self.minValue)/(-1*self.height)

        else:
            ControlBase.OnFocus = None
            
        return esta_encima


















        # Inicializo las superficies del control
        self.background.normal_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.background.hover_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.background.down_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.background.disable_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)

        # Limpio los background
        self.background.normal_image.fill(self.background.normal_color)
        self.background.hover_image.fill(self.background.hover_color)
        self.background.down_image.fill(self.background.down_color)
        self.background.disable_image.fill(self.background.disable_color)
     