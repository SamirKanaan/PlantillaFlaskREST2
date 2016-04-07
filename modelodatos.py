# -*- coding: utf-8 -*-
"""
@author: Samir Kanaan
"""
from inicia import db

# Aquí se definen las tablas de la APP, con las columnas que tendrán, su
# tipo y las formas de crear (__init__) y visualizar (__repr__) un elemento
# de ese tipo.

# Tabla de usuarios
class Usuarios(db.Model):
    __tablename__ = "usuarios"
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email
        
    def __repr__(self):
        # Debe devolver string
        return 'Nombre %r, email %r' % (self.nombre, self.email)
        
        

# Tabla de mensajes (clave externa idAutor)
import datetime
class Mensajes(db.Model):
    __tablename__ = 'mensajes'
    
    id      = db.Column(db.Integer, primary_key=True)
    texto   = db.Column(db.String(200))
    tiempo  = db.Column(db.DateTime)
    idAutor = db.Column(db.Integer, None, db.ForeignKey('usuarios.id'))
    
    def __init__(self, texto, idAutor):
        self.texto   = texto
        self.tiempo  = datetime.datetime.now()
        self.idAutor = idAutor
        
    def __repr__(self):
        # Debe devolver string
        return 'Texto %r, idAutor %r' % (self.texto, self.idAutor)

