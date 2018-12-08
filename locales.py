#! /usr/bin/env python
#-*- coding: UTF-8 -*-

'''Constantes utilizadas para definir distintos conceptos'''

###################################################
##                                               ##
##                 ORIENTACIONES                 ##
##                                               ##
##  Orientación de distintos elementos, como por ##
##  ejemplo los slider, para diferenciar un      ##
##  slider horizontal de uno vertical.           ##
###################################################
O_HORIZONTAL = 0
O_VERTICAL = 1


###################################################
##                                               ##
##                 ALINEACIONES                  ##
##                                               ##
##  Alineacion del texto en aquellos elementos   ##
##  que tienen la propiedad align.               ##
###################################################
A_LEFT = 0
A_RIGHT = 1
A_TOP = 2
A_BOTTOM = 3
A_CENTER = 4
A_TOPLEFT = 5
A_TOPRIGHT = 6
A_BOTTOMLEFT = 7
A_BOTTOMRIGHT = 8


###################################################
##                                               ##
##                   ESTILOS                     ##
##                                               ##
##  Distintos estilos graficos, por ejemplo para ## 
##  los bordes.                                  ##
###################################################
S_SOLID = 0
S_DOT = 1


###################################################
##                                               ##
##                  TIPOS                        ##
##                                               ##
##  Es el tipo de renderizado que se utilizará   ##
##  en las superficies. El tipo T_DRAW dibuja    ##
##  las superficies, el tipo T_IMAGE coloca la   ##
##  imagen indicada sobre la superficie.         ##
###################################################
T_DRAW = 0
T_IMAGE = 1


###################################################
##                                               ##
##               DIRECCIONES                     ##
##                                               ##
##  Direcciones de movimiento, principalmente    ##
##  asociadas con el paso del foco entre los     ##
##  controles de una pantalla, o elementos de un ##
##  mismo control.                               ##
###################################################
D_KEEP = 0  # No permite el movimiento
D_NEXT = 1  # Solo permite moverse hacia el siguiente
D_PREV = 2  # Solo permite moverse hacia el anterior
D_PREVNEXT = 3 # Puede moverse en ambos sentidos


###################################################
##                                               ##
##             BOTONES DEL MOUSE                 ##
##                                               ##
##  Constantes para los botones del mouse        ##
###################################################
M_BUTTON1 = 1
M_BUTTON2 = 2
M_BUTTON3 = 4
