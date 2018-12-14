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

    __screens = {}
    __current = None
    __prev = None


    @staticmethod
    def set_current(name):
        '''Cambia la pantalla actual por la indicada en name'''

        if Screen.__current != None:
            if name != Screen.__current.name:  # Si el nombre de current es igual a la que cambio, entonces no hago nada
                Screen.__prev = Screen.__current
                Screen.__current = Screen.__screens[name]
        else:
            # Si inicialmente el current era None estoy comenzado, entonces inicializo las dos con la pantalla pasada
            Screen.__current = Screen.__screens[name]
            Screen.__prev = Screen.__current




    @staticmethod
    def get_current():
        '''Devuelve la pantalla actual'''
        return Screen.__current


    @staticmethod
    def set_prev():
        '''Cambia la pantalla actual por la anterior'''
        aux = Screen.__current
        Screen.__current = Screen.__prev
        Screen.__prev = aux

    @staticmethod
    def screens():
        '''Devuelve una lista con las pantallas disponibles'''
        return Screen.__screens.values()
    

    def __init__(self, name):

        # Propiedades principales: nombre y controles
        self.__name = name
        self.__controls = {}

        # Establezco el fondo y sus caracteristicas
        self.__background_type = T_DRAW
        self.__background_color = Color.Black
        self.__background_image = None


        # Establezco el foco y sus caracteristicas
        self.__focus = None
        self.__focus_border = Border()

        self.__focus_border.color = Color.Red
        self.__focus_border.size = 1
        self.__focus_border.style = S_SOLID
        self.__focus_border.show = True
        

        # Agrego la pantalla al diccionario. Si ya existe lanzo una excepcion
        if name in Screen.__screens:
            raise screenExistente(name)

        Screen.__screens[name] = self


    # PROPIEDADES
    @property
    def name(self):
        '''Nombre de la pantalla. Solo lectura'''
        return self.__name
    
    @property
    def background_color(self):
        '''Color de fondo para la pantalla'''
        return self.__background_color
    
    
    @background_color.setter
    def background_color(self, color):
        self.__background_color = color
    
    @property
    def background_image(self):
        '''Imagen de fondo para la pantalla cuando se utiliza el fondo de tipo T_IMAGE'''
        return self.__background_image
    
    
    @background_image.setter
    def background_image(self, image):
        self.__background_image = image
    
    @property
    def background_type(self):
        '''Tipo de fondo para la pantalla. Se puede seleccionar entre T_DROW o T_IMAGE'''
        return self.__background_type
    
    
    @background_type.setter
    def background_type(self, tipo):
        self.__background_type = tipo


    @property
    def focus_border(self):
        '''Borde del control que tiene el foco'''
        return self.__focus_border
    
    
    @focus_border.setter
    def focus_border(self, borde):
        self.__focus_border = borde
    
    
    



    # FUNCIONES PARA EL MANEJO DE CONTROLES


    def addControl(self, control):
        '''Agrega el control pasado a la lista de controles de la pantalla'''

        # Agrega el control solo si no existe en el diccionario
        if control.name in self.__controls:  
            raise controlExistente(control.name)

        self.__controls[control.name] = control
        control._Control__screen = self

        # Verifica que el orden del foco en el control sea valido
        fo = [c.focusOrder for c in self.get_controls()]  # Lista de focusOrder usados

        if control.focusOrder in fo: # Si el orden del control ya existe ...
            n = 1
            while n in fo:           # ... Busco un orden nuevo que sea valido ...
                n += 1

            control.focusOrder = n   # ... y se lo asigno al control

    def addControls(self, *controles):
        '''Agrega los controles pasados a la lista de controles de la pantalla'''

        if len(controles)==0:  # Si no paso ningún control lanzo una excepción
            raise TypeError('addControls() takes at least 1 argument (0 given)')

        for control in controles:
            # Agrega el control solo si no existe en el diccionario
            if control.name in self.__controls:  
                raise controlExistente(control.name)

            self.__controls[control.name] = control
            control._Control__screen = self

            # Verifica que el orden del foco en el control sea valido
            fo = [c.focusOrder for c in self.get_controls()]  # Lista de focusOrder usados

            if control.focusOrder in fo: # Si el orden del control ya existe ...
                n = 1
                while n in fo:           # ... Busco un orden nuevo que sea valido ...
                    n += 1

                control.focusOrder = n   # ... y se lo asigno al control




    def removeControl(self, name):
        '''Quita el control de nombre name de la lista de controles de la pantalla y devuelve el control quitado'''

        if name in self.__controls:
            c = self.__controls.pop(name)
            c._Controls__screen = None
            return c
        else:
            raise controlInexistente(name)


    def get_controls(self):
        '''Devuelve una lista con los controles de la pantalla'''
        return self.__controls.values()


    def get_control(self, name, raiseErr=True):
        '''Devuelve el control indicado en name. Si no existe y raiseErr=True lanza una excepcion, de lo contrario devuelve None'''

        if name in self.__controls:
            return self.__controls[name]
        else:
            if raiseErr:
                raise controlInexistente
            else:
                return None



    # FUNCIONES PARA EL MANEJO DEL FOCO

    
    def set_focus(self, control):
        '''Pongo el foco en el control pasado'''
        if control != None:
            if control.focusable and control.enable:
                self.__focus = control

    def get_focus(self):
        '''Devuelvo el control que tiene el foco'''
        return self.__focus

    def focus_next(self):
        '''Pasa el foco al siguiente control de la lista, o al siguiente elemento del control si lo tuviera.'''

        def cmp(x, y): 
            if x.focusOrder < y.focusOrder:
                return -1
            elif x.focusOrder > y.focusOrder:
                return 1
            else:
                return 0

        lo = [ c for c in self.get_controls() if c.focusable and c.enable]
        lo.sort(cmp= cmp)  # Lista ordenada
        
        if self.__focus != None:
            if self.__focus.change_focus(D_NEXT):
                fin = True # Variable auxiliar que me sirve para saber si llegue al final de la lista

                for c in lo:
                    if c.focusOrder > self.__focus.focusOrder:  # Si durante el bucle el focusOrder es mayor que el actual...
                        self.__focus = c                        # ... asigno el encontrado como actual ...
                        fin = False                             # ... cambio la bandera a False para indicar que no llegué hasta el final...
                        break                                   # ... y salgo del bucle


                if fin:                        # Si en el bucle había llegado hasta el final, es xq el focusOrder actual era el mas alto ...
                    self.__focus = lo[0]       # ... y por lo tanto salió del bucle normalmente. En este caso asigno el primer control.

        else:
            self.__focus = lo[0]  # Si no había ningún control en foco, coloco el primero de la lista de orden





    def focus_prev(self):
        '''Pasa el foco al control anterior de la lista, o al elemento anterior del control si lo tuviera.'''

        def cmp(x, y): 
            if x.focusOrder > y.focusOrder:
                return -1
            elif x.focusOrder < y.focusOrder:
                return 1
            else:
                return 0

        lo = [ c for c in self.get_controls() if c.focusable and c.enable]
        lo.sort(cmp=cmp) # Lista ordenada en reversa
        
        if self.__focus != None:
            if self.__focus.change_focus(D_PREV):
                fin = True # Variable auxiliar que me sirve para saber si llegue al final de la lista
            
                for c in lo:
                    if c.focusOrder < self.__focus.focusOrder:  # Si durante el bucle el focusOrder es menor que el actual...
                        self.__focus = c                        # ... asigno el encontrado como actual ...
                        fin = False                             # ... cambio la bandera a False para indicar que no llegué hasta el final...
                        break                                   # ... y salgo del bucle


                if fin:                        # Si en el bucle había llegado hasta el final, es xq el focusOrder actual era el mas bajo ...
                    self.__focus = lo[0]       # ... y por lo tanto salió del bucle normalmente. En este caso asigno el primer control ...
                                              # ... ya que al estar ordenada en reversa el primer elemento de la lista es el mayor
        else:
            self.__focus = lo[0]  # Si no había ningún control en foco, coloco el primero de la lista de orden


    @property
    def focus_border(self):
        '''Tipo de borde a dibujar para el control con el foco'''
        return self.__focus_border
    
    
    @focus_border.setter
    def focus_border(self, borde):
        self.__focus_border = borde
    
    

    # FUNCIONES DE DIBUJADO

    def render(self, display):
        '''Dibuja todos los controles de la pantalla en el display pasado'''

        for ctl in self.get_controls():
            ctl.render(display)

    def update(self):
        '''Realiza update de todos los controles de la pantalla'''

        for ctl in self.get_controls():
            ctl.update()


    # FUNCIONES ESPECIALES
    def __repr__(self):
        strControles = '\n'
        for n in self.get_controls():
            strControles = strControles + n.name + '\n'

        return 'Pantalla: ' + self.name + '\n Controles: ' + strControles

class Control(pygame.Surface):
    """Clase base de la cual derivan todos los controles. En ésta clase están definidas las propiedades y métodos que
    tienen en común todos los controles. Algunas propiedades y/o métodos definidos aquí deben ser extendidos o 
    redefinidos en la definición propia del control para su correcto funcionamiento.

    El constructor de ésta clase recibe 2 argumentos obligatorios. El primero es un objeto pygame.Rect o una tupla de 4
    enteros que definen la posicion y el tamaño del control. El segundo es un string conteniendo un nombre para el
    control, que debe ser único entre todos los controles."""

    # Propiedades de clase
    __controls = {}


    # Metodos estaticos
    @staticmethod
    def controls(name):
        '''Devuelve el control con nombre name, de entre todos los controles creados'''
        return __controls[name]



    def __init__(self, rect, name):

        super(Control, self).__init__((rect[2], rect[3]), pygame.HWSURFACE|pygame.SRCALPHA)

        if name in Control.__controls:
            raise controlExistente(name)

        self.__name = name
        self.__pos = (rect[0], rect[1])
        self.__size = (rect[2], rect[3])
        self.__border = Border()
        self.__visible = True
        self.__enable = True
        self.__focusable = True
        self.__screen = None    #  Inicialmente no tiene pantalla
        self.__background = Layer()
        self.__midground = Layer()
        self.__foreground = Layer()
        self.__font = Font('Default')
        self.__tag = None
        self.__focusOrder = 0

        

    # PROPIEDADES

    @property
    def name(self):
        '''Nombre del control. Solo lectura'''
        return self.__name

    @property
    def pos(self):
        '''Posicion del control'''
        return self.__pos
        
    @pos.setter
    def pos(self, val):
        self.__pos = val

    @property
    def left(self):
        '''Devuelve el borde izquierdo'''
        return self.__pos[0]

    @property
    def right(self):
        '''Devuelve el borde derecho'''
        return self.__pos[0]+__size[0]
    
    @property
    def top(self):
        '''Devuelve el borde superior'''
        return self.__pos[1]

    @property
    def bottom(self):
        '''Devuelve el borde inferior'''
        return self.__pos[1]+__size[1]
    
    
    @property
    def size(self):
        '''Tamaño del control. Solo lectura'''
        return self.__size

    def get_rect(self):
        '''Devuelve un objeto pygame.Rect() con el rectángulo del control'''

        # Este método sobreescribe la funcion del mismo nombre de la clase pygame.Surface()
        return pygame.Rect(self.pos, self.size)

    @property
    def border(self):
        '''Objeto de tipo Border() para definir el borde del control'''
        return self.__border
        
    @border.setter
    def border(self, val):
        self.__border = val

    @property
    def visible(self):
        '''Indica si el control se debe dibujar o no'''
        return self.__visible
        
    @visible.setter
    def visible(self, val):
        self.__visible = val
    
    
    @property
    def enable(self):
        '''Indica si el control puede interactuar con el usuario'''
        return self.__enable
        
    @enable.setter
    def enable(self, val):
        self.__enable = val
    

    @property
    def focusable(self):
        '''Indica si el control puede obtener el foco'''
        return self.__focusable
        
    @focusable.setter
    def focusable(self, val):
        self.__focusable = val
    
    
    @property
    def screen(self):
        '''Pantalla a la que pertenece el control. Solo lectura'''
        return self.__screen
      

    @property
    def background(self):
        '''Capa de fondo del control'''
        return self.__background
        
    @background.setter
    def background(self, val):
        self.__background = val
    
    @property
    def midground(self):
        '''Capa del medio del control'''
        return self.__midground
    
    
    @midground.setter
    def midground(self, val):
        self.__midground = val
    

    @property
    def foreground(self):
        '''Capa frontal del control'''
        return self.__foreground
        
    @foreground.setter
    def foreground(self, val):
        self.__foreground = val
    
    @property
    def font(self):
        '''Fuente a usar con el texto del control'''
        return self.__font
        
    @font.setter
    def font(self, val):
        self.__font = val

    # @property
    # def font_color(self):
    #     '''Color que se utilizara en el texto del control'''
    #     return self.__font_color
    
    
    # @font_color.setter
    # def font_color(self, val):
    #     self.__font_color = val
    
    
    
    @property
    def tag(self):
        '''Propiedad utilizada para guardar cualquier tipo de dato'''
        return self.__tag
        
    @tag.setter
    def tag(self, val):
        self.__tag = val
    
    @property
    def focusOrder(self):
        '''Entero mayor o igual que 0 con el orden de obtención del foco. No pueden haber dos números iguales en una 
        misma pantalla, de ser así esta propiedad se modificará automáticamente al agregarla a la pantalla asignada.'''
        return self.__focusOrder
        
    @focusOrder.setter
    def focusOrder(self, val):
        if val < 0: 
            val = 0
        self.__focusOrder = val
    
                                        
   
    # VERIFICACIONES

    def is_hover(self):
        '''Devuelve un entero indicando si el mouse está sobre el control. Si el resultado es 0 el mouse se encuentra
        fuera del control, si es distinto de 0 está sobre el control.'''

        # Si el control tiene varias zonas interactivas extender esta función para que devuelva un entero distinto de 0
        # indicando sobre que zona se encuentra. 

        if self.visible:  
            return int(self.get_rect().collidepoint(pygame.mouse.get_pos()))

    def is_down(self):
        '''Devuelve un entero indicando si algún botón del mouse está presionado sobre el control. Si el resultado es 0
        no hay ningún botón presionado. De ser distinto de 0, el número obtenido indica que botón hay presionado. 
        Notar que si hay mas de un botón presionado el resultado será la suma de ambos botones.
        Los posibles valores obtenidos son los siguientes:
                          Ninguno = 0
                             Left = 1
                            Right = 2
                     Left + Right = 3
                           Middle = 4
                    Middle + Left = 5
                   Middle + Right = 6
            Middle + Left + Right = 7
            '''
        if self.is_hover() and self.enable:

            btns = pygame.mouse.get_pressed()

            return (int(btns[0]) + int(btns[1])*2 + int(btns[2])*4)
        else:   
            return 0
            

    def is_focus(self):
        '''Devuelve True si el foco está situado sobre el control, de lo contrario devuelve False'''

        return self == self.screen.get_focus()

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

    def update(self):
        '''Actualiza los gráficos del control. Debe llamarse a este método cuando cambia alguna propiedad relacionada a 
        los gráficos'''
        
        # Inicializo las superficies del control
        self.background.normal_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.background.hover_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.background.down_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.background.disable_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)

        self.midground.normal_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.midground.hover_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.midground.down_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.midground.disable_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)

        self.foreground.normal_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.foreground.hover_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.foreground.down_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.foreground.disable_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)

        # Limpio los background
        self.background.normal_image.fill(self.background.normal_color)
        self.background.hover_image.fill(self.background.hover_color)
        self.background.down_image.fill(self.background.down_color)
        self.background.disable_image.fill(self.background.disable_color)
        # Los midground son transparentes
        self.midground.normal_image.fill(Color.Transparent)
        self.midground.hover_image.fill(Color.Transparent)
        self.midground.down_image.fill(Color.Transparent)
        self.midground.disable_image.fill(Color.Transparent)
        # Los foreground tambien son transparentes
        self.foreground.normal_image.fill(Color.Transparent)
        self.foreground.hover_image.fill(Color.Transparent)
        self.foreground.down_image.fill(Color.Transparent)
        self.foreground.disable_image.fill(Color.Transparent)



        # Dibuja el borde del control

        if self.border.show:
              # Normal
            pygame.draw.rect(self.midground.normal_image, self.border.color, (0,0,self.get_width(),self.get_height()), self.border.size)
              # Hover
            pygame.draw.rect(self.midground.hover_image, self.border.color, (0,0,self.get_width(),self.get_height()),self.border.size)
              # Down
            pygame.draw.rect(self.midground.down_image, self.border.color, (0,0,self.get_width(),self.get_height()),self.border.size)
              # Disable
            pygame.draw.rect(self.midground.disable_image, self.border.color, (0,0,self.get_width(),self.get_height()),self.border.size)




    def render(self, display):
        '''Dibuja el control en el display pasado'''
        
        if self.visible:
            if not self.enable:
                display.blit(self.background.disable_image, self.pos)
                display.blit(self.midground.disable_image, self.pos)
                display.blit(self.foreground.disable_image, self.pos)
            else:
                if self.is_hover():
                    if self.is_down():
                        display.blit(self.background.down_image, self.pos)
                        display.blit(self.midground.down_image, self.pos)
                        display.blit(self.foreground.down_image, self.pos)
                    else:
                        display.blit(self.background.hover_image, self.pos)
                        display.blit(self.midground.hover_image, self.pos)
                        display.blit(self.foreground.hover_image, self.pos)
                else:
                    display.blit(self.background.normal_image, self.pos)
                    display.blit(self.midground.normal_image, self.pos)
                    display.blit(self.foreground.normal_image, self.pos)

            # Dibujo el rectángulo que indica que tiene el foco
            if self.is_focus(): 
                pygame.draw.rect(display, self.screen.focus_border.color, (self.left, self.top ,self.get_width(),self.get_height()), self.screen.focus_border.size)

            return True
        else:
            return False






    def click(self, boton=None):
        '''Método a llamar cuando se hace click. Devuelve 1 si está encima del control, de lo contrario devuelve 0'''

        ##### IMPORTANTE: Esta funcion debe sobreescribirse en todas las clases derivadas que requieran controlar el click       
       
        hover = self.is_hover() # Guardo el resultado para no llamar a is_hover() 2 veces

        if hover:
            if self.enable:
                if self.focusable:
                    self.screen.set_focus(self)
            
        else:
            self.screen.set_focus(None)
            
        return hover



    def keydown(self, k=None):
        '''Método a llamar cuando se presiona una tecla'''
        pass


    # METODOS Y FUNCIONES PARA MANEJO DE LA PANTALLA DEL CONTROL

    def drop_screen(self):
        '''Desvincula el control de cualquier pantalla'''
        if self.__screen != None:
            self.__screen.removeControl(self.name) # Este método del objeto Screen automáticamente coloca None en _screen

    def get_screen(self):
        '''Obtiene la pantalla del control. Es el mismo resultado que la propiedad screen'''
        return self.screen

    def set_screen(self, pantalla):
        '''Asigna el control a la pantalla pasada'''

        # Solo se puede asignar a una pantalla cuando no pertenece a ninguna. Si ya es parte de una pantalla debe
        # dejarla antes de pertenecer a otra. Cada control solo puede formar parte de una pantalla
        if self.__screen == None:
            pantalla.addControl(self) # Este método del objeto Screen asigna automáticamente la pantalla a _screen

        else:
            raise screenAsignada(self.name)


    # FUNCIONES ESPECIALES

    def __repr__(self):

        return 'Control ' + self.name + ' perteneciente a la pantalla ' + self.screen.name


class Button(Control):
    '''Control de tipo botón. Recibe 3 parámetros, un Rect con su tamaño y posicion, un nombre que debe ser único, y 
    una función que se ejecutará cuando se haga click sobre él. Otra propiedad importante es caption, que es el
    texto que se muestra sobre el control, y que por defecto es igual al nombre del control. El texto se dibuja con
    los colores del foreground'''

    def __init__(self, rect, name, action):
        super(Button, self).__init__(rect, name)
        self.__action = action
        self.__caption = name
        self.__align = A_CENTER

    @property
    def caption(self):
        '''Texto que se muestra sobre el botón'''
        return self.__caption
    
    
    @caption.setter
    def caption(self, val):
        self.__caption = val

    @property
    def action(self):
        '''Función a ejecutar cuando se hace click sobre el botón. Solo lectura'''
        return self.__action

    @property
    def align(self):
        '''Alineación del texto en el botón'''
        return self.__align
    
    
    @align.setter
    def align(self, val):
        self.__align = val
    
    


    def click(self, boton=None):
        '''Método a llamar cuando se hace click. Devuelve 1 si está encima del control, de lo contrario devuelve 0'''
       
        hover = self.is_hover() # Guardo el resultado para no llamar a is_hover() 2 veces

        if hover and self.enable and self.focusable:
            self.screen.set_focus(self)
            self.action()
            
        else:
            self.screen.set_focus(None)
            
        return hover
        

    def update(self):
        '''Actualiza los gráficos del control'''
        super(Button, self).update()

        # Texto renderizado
        imgtexto = self.font.render(self.caption, True)
        
        # Obtiene las dimensiones del texto
        imgtextoWidth, imgtextoHeight = self.font.size(self.caption) 

        # Calculo la posicion
            # Valor del usuario
        if self.align == A_MANUAL:
            posX, posY = self.__pos_text
        
            # Posicion X
        if self.align == A_LEFT or self.align == A_TOPLEFT or self.align == A_BOTTOMLEFT:
            posX = 0
        
        if self.align == A_CENTER or self.align == A_TOP or self.align == A_BOTTOM:
            posX = self.get_width()/2 - imgtextoWidth/2

        if self.align == A_RIGHT or self.align == A_BOTTOMRIGHT or self.align == A_TOPRIGHT:
            posX = self.get_width() - imgtextoWidth 

            # Posicion Y
        if self.align == A_TOPLEFT or self.align == A_TOP or self.align == A_TOPRIGHT:
            posY = 0
        
        if self.align == A_CENTER or self.align == A_LEFT or self.align == A_RIGHT:
            posY = self.get_height()/2 - imgtextoHeight/2

        if self.align == A_BOTTOMLEFT or self.align == A_BOTTOMRIGHT or self.align == A_BOTTOM:
            posY = self.get_height() - imgtextoHeight


        # Dibuja el texto sobre las superficies del midground
        self.midground.normal_image.blit(imgtexto, (posX, posY))
        self.midground.hover_image.blit(imgtexto, (posX, posY))
        self.midground.down_image.blit(imgtexto, (posX, posY))
        self.midground.disable_image.blit(imgtexto, (posX, posY))

        # Dibuja el borde del control, para que no quede por detras de los textos

        if self.border.show:
              # Normal
            pygame.draw.rect(self.midground.normal_image, self.border.color, (0,0,self.get_width(),self.get_height()), self.border.size)
              # Hover
            pygame.draw.rect(self.midground.hover_image, self.border.color, (0,0,self.get_width(),self.get_height()),self.border.size)
              # Down
            pygame.draw.rect(self.midground.down_image, self.border.color, (0,0,self.get_width(),self.get_height()),self.border.size)
              # Disable
            pygame.draw.rect(self.midground.disable_image, self.border.color, (0,0,self.get_width(),self.get_height()),self.border.size)


class Label(Control):
    '''Control para mostrar un texto sin interacción con el usuario'''

    def __init__(self, rect, name, texto):
        super(Label, self).__init__(rect, name)

        # Configuracion del texto
        self.__text = texto
        self.__align = A_CENTER
        self.__pos_text = (0,0)


        # Como un label no interactúa con el usuario, lo primero es hacer que no reciba el foco, y ademas el normal, hover y down deben ser 
        # del mismo color. Este comportamiento puede ser cambiado por el usuario
        self.focusable = False  # El label no puede recibir el foco
        col = self.background.normal_color
        self.background.hover_color = col
        self.background.down_color = col



    @property
    def text(self):
        '''Texto del Label'''
        return self.__text

    @text.setter
    def text(self, texto):
        
        self.__text = texto

    @property
    def pos_text(self):
        '''Posición del texto cuando se setea la alineación manual'''
        return self.__pos_text
    
    
    @pos_text.setter
    def pos_text(self, val):
        self.__pos_text = val


    @property
    def align(self):
        '''Alineación del texto'''
        return self.__align
    
    
    @align.setter
    def align(self, val):
        self.__align = val


    def update(self):
        '''Actualiza los gráficos del control'''

        super(Label, self).update()

        # Texto renderizado
        imgtexto = self.font.render(self.text, True)
        
        # Obtiene las dimensiones del texto
        imgtextoWidth, imgtextoHeight = self.font.size(self.text) 

        # Calculo la posicion
            # Valor del usuario
        if self.align == A_MANUAL:
            posX, posY = self.__pos_text
        
            # Posicion X
        if self.align == A_LEFT or self.align == A_TOPLEFT or self.align == A_BOTTOMLEFT:
            posX = 0
        
        if self.align == A_CENTER or self.align == A_TOP or self.align == A_BOTTOM:
            posX = self.get_width()/2 - imgtextoWidth/2

        if self.align == A_RIGHT or self.align == A_BOTTOMRIGHT or self.align == A_TOPRIGHT:
            posX = self.get_width() - imgtextoWidth 

            # Posicion Y
        if self.align == A_TOPLEFT or self.align == A_TOP or self.align == A_TOPRIGHT:
            posY = 0
        
        if self.align == A_CENTER or self.align == A_LEFT or self.align == A_RIGHT:
            posY = self.get_height()/2 - imgtextoHeight/2

        if self.align == A_BOTTOMLEFT or self.align == A_BOTTOMRIGHT or self.align == A_BOTTOM:
            posY = self.get_height() - imgtextoHeight


        # Dibuja el texto sobre las superficies del midground
        self.midground.normal_image.blit(imgtexto, (posX, posY))
        self.midground.hover_image.blit(imgtexto, (posX, posY))
        self.midground.down_image.blit(imgtexto, (posX, posY))
        self.midground.disable_image.blit(imgtexto, (posX, posY))

        # Dibuja el borde del control, para que no quede por detras de los textos

        if self.border.show:
              # Normal
            pygame.draw.rect(self.midground.normal_image, self.border.color, (0,0,self.get_width(),self.get_height()), self.border.size)
              # Hover
            pygame.draw.rect(self.midground.hover_image, self.border.color, (0,0,self.get_width(),self.get_height()),self.border.size)
              # Down
            pygame.draw.rect(self.midground.down_image, self.border.color, (0,0,self.get_width(),self.get_height()),self.border.size)
              # Disable
            pygame.draw.rect(self.midground.disable_image, self.border.color, (0,0,self.get_width(),self.get_height()),self.border.size)




class Image(Control):
    '''Contenedor para mostrar una imagen'''

    def __init__(self, rect, name, imagen=None):
        super(Image, self).__init__(rect, name)
        self.__image = imagen
        self.__align = A_CENTER
        self.__pos_image = (0, 0)


        # Como no interactúa con el usuario, lo primero es hacer que no reciba el foco, y ademas el normal, hover y down deben ser 
        # del mismo color, que será transparente por default. Este comportamiento puede ser cambiado por el usuario
        self.focusable = False  # El label no puede recibir el foco
        self.background.normal_color = Color.Transparent
        self.background.hover_color = Color.Transparent
        self.background.down_color = Color.Transparent

        # Por defecto no se mostrará el borde
        self.border.show = False


    @property
    def image(self):
        '''Imagen que mostrará el control'''
        return self.__image
    
    
    @image.setter
    def image(self, val):
        self.__image = val
    
    @property
    def pos_image(self):
        '''Posición de la imagen'cuando se setea la alineacón manual'''
        return self.__pos_image
    
    
    @pos_image.setter
    def pos_image(self, val):
        self.__pos_image = val

    @property
    def align(self):
        '''Alineación de la imagen'''
        return self.__align
    
    
    @align.setter
    def align(self, val):
        self.__align = val
    
    
    
    
    def load_image(self, path):
        '''Carga una imagen en el control desde un archivo. Los tipos de archivo soportados son los siguientes:
            *  JPG
            *  PNG
            *  GIF (no-animado)
            *  BMP
            *  PCX
            *  TGA (sin comprimir)
            *  TIF
            *  LBM
            *  PBM
            *  PGM
            *  PPM
            *  XPM

           Nota: El control no se redimensiona al cargar la imagen. Para que el control tenga el mismo tamaño debe ser
           creado inicialmente con el tamaño correcto. Se sugieren los siguientes codigos para conseguir esto:

           Caso 1:
                imagen_control = pygame.image.load("img.png")
                control_img = Image(imagen_control.get_rect(topleft=(posX, posY)), nombre_control, imagen_control)
                
                Notar que imagen_control es un objeto pygame.Surface()

           Caso 2:
                rect_control = (posX, posY, img_width, img_height)  # Las dimensiones de la imagen deben conocerse de antemano
                control_img = Image(rect_control, nombre_control)
                control_img.load_image("img.png") '''

        self.image = pygame.image.load(path)
        return self.image


    def fit_image(self):
        '''Ajusta la imagen a las dimensiones del control. Esto no modifica las dimensiones del control. Luego de llamar
        a esta funcion se debe llamar a update() para que tengan efecto los cambios.'''

        if self.image != None:
            # El mismo tamño del control, las mismas caracteristicas que la imagen actual
            #print self.size
            #print self.image
            nueva = pygame.Surface(self.size, 0, self.image)  
            pygame.transform.smoothscale(self.image, self.size, nueva)
            self.image = nueva
            return self.image

    def update(self):
        '''Actualiza los gráficos del control'''
        super(Image, self).update()
        
        # Obtiene las dimensiones de la imagen
        if self.image == None:
            self.image = pygame.Surface(self.get_size(), pygame.HWSURFACE|pygame.SRCALPHA)
            self.image.fill(Color.Transparent)

        imgWidth, imgHeight = self.image.get_size() 

        # Calculo la posicion
            # Valor del usuario
        if self.align == A_MANUAL:
            posX, posY = self.__pos_image
        
            # Posicion X
        if self.align == A_LEFT or self.align == A_TOPLEFT or self.align == A_BOTTOMLEFT:
            posX = 0
        
        if self.align == A_CENTER or self.align == A_TOP or self.align == A_BOTTOM:
            posX = self.get_width()/2 - imgWidth/2

        if self.align == A_RIGHT or self.align == A_BOTTOMRIGHT or self.align == A_TOPRIGHT:
            posX = self.get_width() - imgWidth 

            # Posicion Y
        if self.align == A_TOPLEFT or self.align == A_TOP or self.align == A_TOPRIGHT:
            posY = 0
        
        if self.align == A_CENTER or self.align == A_LEFT or self.align == A_RIGHT:
            posY = self.get_height()/2 - imgHeight/2

        if self.align == A_BOTTOMLEFT or self.align == A_BOTTOMRIGHT or self.align == A_BOTTOM:
            posY = self.get_height() - imgHeight


        # Dibuja el texto sobre las superficies del midground
        self.midground.normal_image.blit(self.image, (posX, posY))
        self.midground.hover_image.blit(self.image, (posX, posY))
        self.midground.down_image.blit(self.image, (posX, posY))
        self.midground.disable_image.blit(self.image, (posX, posY))

        # Dibuja el borde del control, para que no quede por detras de los textos

        if self.border.show:
              # Normal
            pygame.draw.rect(self.midground.normal_image, self.border.color, (0,0,self.get_width(),self.get_height()), self.border.size)
              # Hover
            pygame.draw.rect(self.midground.hover_image, self.border.color, (0,0,self.get_width(),self.get_height()),self.border.size)
              # Down
            pygame.draw.rect(self.midground.down_image, self.border.color, (0,0,self.get_width(),self.get_height()),self.border.size)
              # Disable
            pygame.draw.rect(self.midground.disable_image, self.border.color, (0,0,self.get_width(),self.get_height()),self.border.size)



###########################################################################################################################################
###########################################################################################################################################
#####                                                                                                                                 #####
#####                                 Hasta acá lo que corresponde al primer release (v0.0.1)                                         #####
#####                                                                                                                                 #####
###########################################################################################################################################
###########################################################################################################################################



class CheckBox(Control):
    '''Caja de verificacion'''

    def __init__(self, rect, name, value=False):
        super(CheckBox, self).__init__(rect, name)
        
        # Valor del CheckBox
        self.__value = value

        # Capas intermedias para tener los gráficos checked, unchecked. (ver método render)
        self.__checked = Layer()
        self.__unchecked = Layer()

        # Puntos que definen la marca de checked
        self.__p1 = (self.get_width()*0.2, self.get_height()*0.5)
        self.__p2 = (self.get_width()*0.4, self.get_height()*0.8)
        self.__p3 = (self.get_width()*0.8, self.get_height()*0.25)

        # Caracteristicas de la marca
        self.__border_mark_normal = Border()
        self.__border_mark_normal.color = Color.ForestGreen
        self.__border_mark_normal.size = 4
        self.__border_mark_hover = Border()
        self.__border_mark_hover.color = Color.DarkSeaGreen
        self.__border_mark_hover.size = 8
        self.__border_mark_down = Border()
        self.__border_mark_down.color = Color.LightGreen
        self.__border_mark_down.size = 8
        self.__border_mark_disable = Border()
        self.__border_mark_disable.color = Color.Gray
        self.__border_mark_disable.size = 4



    @property
    def value(self):
        '''Propiedad para establecer el estado del check'''
        return self.__value

    @value.setter
    def value(self, val):
        self.__value = val


    @property
    def border_mark_normal(self):
        '''Tipo de borde para dibujar la marca de checked normal'''
        return self.__border_mark_normal
    
    
    @border_mark_normal.setter
    def border_mark_normal(self, val):
        self.__border_mark_normal = val

    @property
    def border_mark_hover(self):
        '''Tipo de borde para dibujar la marca de checked hover'''
        return self.__border_mark_hover
    
    
    @border_mark_hover.setter
    def border_mark_hover(self, val):
        self.__border_mark_hover = val
    
    @property
    def border_mark_down(self):
        '''Tipo de borde para dibujar la marca de checked down'''
        return self.__border_mark_down
    
    
    @border_mark_down.setter
    def border_mark_down(self, val):
        self.__border_mark_down = val

    @property
    def border_mark_disable(self):
        '''Tipo de borde para dibujar la marca de checked disable'''
        return self.__border_mark_disable
    
    
    @border_mark_disable.setter
    def border_mark_disable(self, val):
        self.__border_mark_disable = val
    
    
    
    


    def update(self):
        '''Actualiza como se mostrara nuestro control segun el modo grafico establecido'''

        # Dibujo los bords con la llamada a la funcion de la clase base
        super(CheckBox, self).update()


        # Superficies para  checked
        self.__checked.normal_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.__checked.hover_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.__checked.down_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.__checked.disable_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.__checked.normal_image.fill(Color.Transparent)
        self.__checked.hover_image.fill(Color.Transparent)
        self.__checked.down_image.fill(Color.Transparent)
        self.__checked.disable_image.fill(Color.Transparent)

        # Superficies para unchecked. En la version dibujada no tiene importancia, pero cobra valor en la version gráfica
        self.__unchecked.normal_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.__unchecked.hover_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.__unchecked.down_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.__unchecked.disable_image = pygame.Surface(self.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.__unchecked.normal_image.fill(Color.Transparent)
        self.__unchecked.hover_image.fill(Color.Transparent)
        self.__unchecked.down_image.fill(Color.Transparent)
        self.__unchecked.disable_image.fill(Color.Transparent)


        # Dibujo el checked
        pygame.draw.line(self.__checked.normal_image, self.__border_mark_normal.color, self.__p1, self.__p2, self.__border_mark_normal.size)
        pygame.draw.line(self.__checked.hover_image, self.__border_mark_hover.color, self.__p1, self.__p2, self.__border_mark_hover.size)
        pygame.draw.line(self.__checked.down_image, self.__border_mark_down.color, self.__p1, self.__p2, self.__border_mark_down.size)
        pygame.draw.line(self.__checked.disable_image, self.__border_mark_disable.color, self.__p1, self.__p2, self.__border_mark_disable.size)
        pygame.draw.line(self.__checked.normal_image, self.__border_mark_normal.color, self.__p2, self.__p3, self.__border_mark_normal.size)
        pygame.draw.line(self.__checked.hover_image, self.__border_mark_hover.color, self.__p2, self.__p3, self.__border_mark_hover.size)
        pygame.draw.line(self.__checked.down_image, self.__border_mark_down.color, self.__p2, self.__p3, self.__border_mark_down.size)
        pygame.draw.line(self.__checked.disable_image, self.__border_mark_disable.color, self.__p2, self.__p3, self.__border_mark_disable.size)

        # Dibujo el unchecked
        # pygame.draw.line(self.__unchecked.normal_image, self.__border_mark_normal.color, self.__p2, self.__p3, self.__border_mark_normal.size)
        # pygame.draw.line(self.__unchecked.hover_image, self.__border_mark_hover.color, self.__p2, self.__p3, self.__border_mark_hover.size)
        # pygame.draw.line(self.__unchecked.down_image, self.__border_mark_down.color, self.__p2, self.__p3, self.__border_mark_down.size)
        # pygame.draw.line(self.__unchecked.disable_image, self.__border_mark_disable.color, self.__p2, self.__p3, self.__border_mark_disable.size)
        # pygame.draw.line(self.__unchecked.normal_image, self.__border_mark_normal.color, self.__p3, self.__p1, self.__border_mark_normal.size)
        # pygame.draw.line(self.__unchecked.hover_image, self.__border_mark_hover.color, self.__p3, self.__p1, self.__border_mark_hover.size)
        # pygame.draw.line(self.__unchecked.down_image, self.__border_mark_down.color, self.__p3, self.__p1, self.__border_mark_down.size)
        # pygame.draw.line(self.__unchecked.disable_image, self.__border_mark_disable.color, self.__p3, self.__p1, self.__border_mark_disable.size)
    

        # Dibuja el borde del control
        if self.border.show:
              # Normal
            pygame.draw.rect(self.__checked.normal_image, self.border.color, (0,0,self.get_width(),self.get_height()), self.border.size)
            pygame.draw.rect(self.__unchecked.normal_image, self.border.color, (0,0,self.get_width(),self.get_height()), self.border.size)
              # Hover
            pygame.draw.rect(self.__checked.hover_image, self.border.color, (0,0,self.get_width(),self.get_height()),self.border.size)
            pygame.draw.rect(self.__unchecked.hover_image, self.border.color, (0,0,self.get_width(),self.get_height()),self.border.size)
              # Down
            pygame.draw.rect(self.__checked.down_image, self.border.color, (0,0,self.get_width(),self.get_height()),self.border.size)
            pygame.draw.rect(self.__unchecked.down_image, self.border.color, (0,0,self.get_width(),self.get_height()),self.border.size)
              # Disable
            pygame.draw.rect(self.__checked.disable_image, self.border.color, (0,0,self.get_width(),self.get_height()),self.border.size)
            pygame.draw.rect(self.__unchecked.disable_image, self.border.color, (0,0,self.get_width(),self.get_height()),self.border.size)


    def render(self, display):
        '''Dibuja el control en la superficie pasada'''

        # Verifico el estado, para saber cual dibujar
        if self.__value :
            self.midground = self.__checked
        else:
            self.midground = self.__unchecked


        return super(CheckBox, self).render(display)




    def click(self, boton=None):
        '''Cambia el valor del control'''
        es_click = super(CheckBox, self).click(boton)

        if es_click and self.enable:
            self.value = not self.__value 

        return es_click





class TextBox(Control): 
    '''Caja de texto'''
    __tiempo = pygame.time.get_ticks() # Para usar en el parpadeo del cursor
    __parpadeo = True # Para usar en el parpadeo del cursor

    def __init__(self, rect, name, texto=""):

        super(TextBox, self).__init__(rect, name)

        self.__text = texto
        self.__cursor = Border()
        self.__cursor.size = 1
        self.__cursorVisible = True
        self.__cursorFreq = 300
        self.__cursorPos = len(texto)
        self.__pos_text = (5,0)
        self.__align = A_RIGHT

        # Hago blanco los colores del fondo para todos los estados
        self.background.normal_color = Color.White
        self.background.hover_color = Color.White
        self.background.down_color = Color.White

        # Hago transparentes los medioplanos y planos frontales
        self.midground.normal_color = Color.Transparent
        self.midground.hover_color = Color.Transparent
        self.midground.down_color = Color.Transparent
        self.foreground.normal_color = Color.Transparent
        self.foreground.hover_color = Color.Transparent
        self.foreground.down_color = Color.Transparent

        pygame.key.set_repeat(400,100)

    @property
    def align(self):
        '''Alineación del texto'''
        return self.__align
    
    
    @align.setter
    def align(self, val):
        self.__align = val
    
    


    @property
    def text(self):
        '''Texto que contiene el control. A diferencia del Label, este texto puede ser modificado por el usuario, por lo que este
        control es usado como entrada de texto, mientras que el Label es solo de salida de texto'''
        return self.__text
    
    
    @text.setter
    def text(self, texto):
        self.__text = texto
    

        # Construye el bitmap de texto 
        bitmap_normal = self.font.render(texto, True)
        bitmap_hover = self.font.render(texto, True)
        bitmap_down = self.font.render(texto, True)
        bitmap_disable = self.font.render(texto, True, self.midground.disable_color)
        bitmapWidth, bitmapHeight = self.font.size(texto) 

        # Calculo la posicion
            # Valor del usuario
        if self.align == A_MANUAL:
            posX, posY = self.pos_text
            posX += self.border.size
            posY += self.border.size
        
            # Posicion X
        if self.align == A_LEFT or self.align == A_TOPLEFT or self.align == A_BOTTOMLEFT:
            posX = 0 + self.border.size
        
        if self.align == A_CENTER or self.align == A_TOP or self.align == A_BOTTOM:
            posX = self.get_width()/2 - bitmapWidth/2

        if self.align == A_RIGHT or self.align == A_BOTTOMRIGHT or self.align == A_TOPRIGHT:
            posX = self.get_width() - bitmapWidth - self.border.size

            # Posicion Y
        if self.align == A_TOPLEFT or self.align == A_TOP or self.align == A_TOPRIGHT:
            posY = 0 + self.border.size
        
        if self.align == A_CENTER or self.align == A_LEFT or self.align == A_RIGHT:
            posY = self.get_height()/2 - bitmapHeight/2

        if self.align == A_BOTTOMLEFT or self.align == A_BOTTOMRIGHT or self.align == A_BOTTOM:
            posY = self.get_height() - bitmapHeight - self.border.size

        # Dibujo el texto sobre el midground
        self.midground.normal_image.fill(self.midground.normal_color)
        self.midground.normal_image.blit(bitmap_normal, (posX, posY))
        self.midground.hover_image.fill(self.midground.hover_color)
        self.midground.hover_image.blit(bitmap_hover, (posX, posY))
        self.midground.down_image.fill(self.midground.down_color)
        self.midground.down_image.blit(bitmap_down, (posX, posY))
        self.midground.disable_image.fill(self.midground.disable_color)
        self.midground.disable_image.blit(bitmap_disable, (posX, posY))

        


        # Dibuja el borde del control

        if self.border.show:
              # Normal
            pygame.draw.rect(self.midground.normal_image, self.border.color, (0,0,self.get_width(),self.get_height()), self.border.size)
              # Hover
            pygame.draw.rect(self.midground.hover_image, self.border.color, (0,0,self.get_width(),self.get_height()),self.border.size)
              # Down
            pygame.draw.rect(self.midground.down_image, self.border.color, (0,0,self.get_width(),self.get_height()),self.border.size)
              # Disable
            pygame.draw.rect(self.midground.disable_image, self.border.color, (0,0,self.get_width(),self.get_height()),self.border.size)





    @property
    def pos_text(self):
        '''Tupla con la posicion del texto dentro del TextBox.'''
        return self.__pos_text
    
    
    @pos_text.setter
    def pos_text(self, val):
        self.__pos_text = val


    @property
    def cursorPos(self):
        '''Define la posicion del cursor en caracteres'''
        return self.__cursorPos

    @cursorPos.setter
    def cursorPos(self, pos):
        self.__cursorPos = pos
    

    def movCursorIzq(self):
        '''Mueve el cursor un caracter hacia la izquierda'''
        self.__cursorPos -= 1
        if self.__cursorPos < 0:
            self.__cursorPos = 0

        return self.cursorPos


    def movCursorDer(self):
        '''Mueve el cursor un caracter hacia la derecha'''
        self.__cursorPos += 1
        if self.__cursorPos > len(self.text):
            self.__cursorPos = len(self.text)

        return self.cursorPos

    def keydown(self, k=None):

        if self.enable and self.is_focus():
            esKeyDown = True
        else:
            esKeyDown = False


        if esKeyDown:
            if k.key == pygame.K_LEFT:
                self.movCursorIzq()

            elif k.key == pygame.K_RIGHT:
                self.movCursorDer()

            elif k.key == pygame.K_BACKSPACE:
                self.text = self.text[:self.__cursorPos][:-1] + self.text[self.__cursorPos:]
                self.movCursorIzq()

            elif k.key == pygame.K_DELETE:
                self.text = self.text[:self.__cursorPos] + self.text[self.__cursorPos+1:]
            
            else:
                self.text = self.text[:self.__cursorPos] + k.unicode + self.text[self.__cursorPos:]
                if str(k.unicode) != '':  # Verifico que lo que se este presionando no sea solo un mods (shift, ctrl, alt)
                    self.movCursorDer()
            

        return esKeyDown

    def render(self, display):
        '''Dibuja el control en la superficie pasada'''


        textoListo = super(TextBox, self).render(display)

        tiemporTranscurrido = pygame.time.get_ticks() - TextBox.__tiempo
        if tiemporTranscurrido > self.__cursorFreq:
            TextBox.__tiempo = pygame.time.get_ticks()
            TextBox.__parpadeo = not TextBox.__parpadeo

        if  textoListo and self.enable and self.is_focus() and TextBox.__parpadeo and self.__cursor.show:
            anchoTexto, altoTexto = self.font.size(self.__text[0:self.__cursorPos])

            # Defino la posición X del cursor según la alineación
            if self.align == A_MANUAL:
                posXcur = self.left + self.__pos_text[0] + anchoTexto + self.border.size

            elif self.align == A_LEFT or self.align == A_TOPLEFT or self.align == A_BOTTOMLEFT:
                posXcur = self.left + anchoTexto + self.border.size


            elif self.align == A_RIGHT or self.align == A_TOPRIGHT or self.align == A_BOTTOMRIGHT:
                posXcur = self.left + self.get_width() - self.font.size(self.__text)[0] + anchoTexto - self.border.size

            elif self.align == A_CENTER or self.align == A_TOP or self.align == A_BOTTOM:
                posXcur = self.left + self.get_width()/2 - self.font.size(self.__text)[0]/2 + anchoTexto

            # Defino la posición Y del cursor según la alineación
            if self.align == A_MANUAL:
                posYcur0 = self.top + self.__pos_text[1] + self.border.size
                posYcur1 = self.top + self.__pos_text[1] + altoTexto + self.border.size


            elif self.align == A_TOPLEFT or self.align == A_TOP or self.align == A_TOPRIGHT:
                posYcur0 = self.top + self.border.size
                posYcur1 = self.top + altoTexto + self.border.size


            elif self.align == A_LEFT or self.align == A_CENTER or self.align == A_RIGHT:
                posYcur0 = self.top + self.get_height()/2 - altoTexto/2
                posYcur1 = self.top + self.get_height()/2 + altoTexto/2

            elif self.align == A_BOTTOMLEFT or self.align == A_BOTTOM or self.align == A_BOTTOMRIGHT:
                posYcur0 = self.top + self.get_height() - altoTexto - self.border.size
                posYcur1 = self.top + self.get_height() - self.border.size 

            

            if posXcur < self.left + self.get_width():
                pygame.draw.line(display, self.__cursor.color , (posXcur , posYcur0), (posXcur , posYcur1) , self.__cursor.size)

        return textoListo

    def click(self, c=None):  
        ''' '''
        # c es el evento de MOUSEBUTTONDOWN 
        # c.pos -> posicion del click 
        # c.button -> boton del click (1 es el principal, 2 es secundario, 3 es central, 4 es rueda arriba, 5 es rueda abajo)
         
        #super(Textbox, self).click(c, screen)

        hover = super(TextBox, self).click(c) 
        
        if hover:
            posClick = c.pos

            dimText = self.font.size(self.__text)

            # Defino la posición del cursor según la alineación. iniText será el pixel horizontal donde inicia el texto, contando desde el
            # lado izquierdo del control
            if self.align == A_MANUAL:
                iniText = self.__pos.text[0]  

            elif self.align == A_LEFT or self.align == A_TOPLEFT or self.align == A_BOTTOMLEFT:
                iniText = 0

            elif self.align == A_RIGHT or self.align == A_TOPRIGHT or self.align == A_BOTTOMRIGHT:
                iniText = self.get_width() - dimText[0]

            elif self.align == A_CENTER or self.align == A_TOP or self.align == A_BOTTOM:
                iniText = self.get_width()/2 - dimText[0]/2



            # Analizo donde se produjo el click

            if posClick[0] > self.left + iniText + dimText[0]:
                self.__cursorPos = len(self.__text)
                return hover
            
            if posClick[0] < self.left + iniText:
                self.__cursorPos = 0
                return hover

            else:
                tamizqant = 0

                for i in range(0,len(self.__text)+1):
                    izq = self.__text[0:i]
                    tamizq = self.font.size(izq)[0]
                    if posClick[0] > self.left + iniText + tamizqant + (tamizq-tamizqant)/2:
                        tamizqant = tamizq
                    else:    
                        self.__cursorPos = len(izq) -1
                        break    

        return hover
