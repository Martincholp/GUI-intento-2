#! /usr/bin/env python
#-*- coding: UTF-8 -*-

'''Modulo conteniendo excepciones personalizadas para la librería'''

# EXCEPCIONES DE CONTROLES

class controlExistente(Exception):
    """Excepción que se lanza al intentar crear un control con un nombre existente en la lista de controles."""
    def __init__(self, name):
        self.name = name

        
    def __str__(self):
        return "Ya existe un control de nombre " + self.name


class controlInexistente(Exception):
    """Excepción que se lanza al intentar obtener un control con un nombre inexistente en la lista de controles."""
    def __init__(self, name):
        self.name = name

        
    def __str__(self):
        return "No existe un control de nombre " + self.name


# EXCEPCIONES DE PANTALLAS

class screenExistente(Exception):
    """Excepción que se lanza al intentar crear una screen con un nombre existente en la lista de screens."""
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return "Ya existe una screen de nombre " + self.name


class screenInexistente(Exception):
    """Excepción que se lanza al intentar obtener una screen con un nombre inexistente en la lista de screens."""
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return "No existe una screen de nombre " + self.name

class screenAsignada(Exception):
    """Excepción que se lanza al intentar asignar una pantalla a un control que ya tiene una."""
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return "El control " + self.name + " ya tiene una pantalla asignada"

