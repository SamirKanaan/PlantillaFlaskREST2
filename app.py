#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 19:35:19 2016

@author: samir
"""

# RESTful API + postgreSQL DB usando SQLAlchemy

from flask import Flask
from flask.ext.restful import Api, Resource
from flask.ext.sqlalchemy import SQLAlchemy

# Crear app y conectar a db
from inicia import app, db

api = Api(app)

# Importar las clases del modelo de datos
from modelodatos import Usuarios, Mensajes


# Falta exigir identificación a los usuarios

from flask import request

# GESTIÓN DE USUARIOS
class ListaUsuariosAPI(Resource):
    def get(self):
        usrs = Usuarios.query.all()
        # Devolver aquí atribs o añadir un método a Usuarios. No hace falta
        # devolver todos los datos (password, id)
        return [{'id':u.id, 'nombre':u.nombre, 'email':u.email} for u in usrs]
    
    # Cambia el nombre o el correo de un usuario, lo que haya en el mensaje
    # El usuario se identifica por su id
    def put(self):
        # Obtener el usuario a modificar, cambiar los valores recibidos y
        # grabarlos en la BD
        usuario = Usuarios.query.filter_by(id=request.json['id']).first()
        
        # Verificar que el usuario existe, si no terminar
        if usuario == None:
            return {"error": "Usuario (id) no encontrado"}, 404

        
        if 'nombre' in request.json:
            usuario.nombre = request.json['nombre']
        if 'email' in request.json:
            usuario.email = request.json['email']

        # Forma más sencilla de actualizar un solo campo:
        # Usuarios.query.filter_by(email=email).update({Usuarios.nombre:nombre})

        try:
            db.session.commit()
            return {'result': True}
        except:
            db.session.rollback()
            return {"error": "Error al modificar el usuario"}, 401
            
    
    # Extraer nombre y email de la petición, crear un usuario, añadirlo a la 
    # bd y devolver éxito, o mensaje+código de error si falla y cancelar petición bd
    def post(self):
        usuario = Usuarios(request.json['nombre'], request.json['email'])
        db.session.add(usuario)
        try:    
            db.session.commit()
            return {'result': True}
        except:
            db.session.rollback()
            return {"error": "Error al añadir el usuario (email ya existe)"}, 401
    
    # Borrar el usuario con un email. Si no existe no produce error, 
    # simplemente no hace nada
    def delete(self):
        email = request.json['email']
        try:
            Usuarios.query.filter_by(email=email).delete()
            db.session.commit()
            return {'result': True}
        except:
            db.session.rollback()
            return {"error": "Error al borrar el usuario"}, 404
          
 
# GESTIÓN DE LOS MENSAJES
class MensajesAPI(Resource):
    def get(self):
        msjs = Mensajes.query.all()
        # Devolver aquí atribs o añadir un método a Usuarios. No hace falta
        # devolver todos los datos (password, id)
        return [{'id':m.id, 'texto':m.texto, 'tiempo':str(m.tiempo), 'autor':m.idAutor} for m in msjs]
    
    # No se pueden modificar los mensajes
    def put(self):
        pass
    
    # Añade un nuevo mensaje
    def post(self):
        msj = Mensajes(request.json['texto'], request.json['autor'])
        db.session.add(msj)
        try:    
            db.session.commit()
            return {'result': True}
        except:
            db.session.rollback()
            return {"error": "Error al añadir el mensaje (autor no valido)"}, 404
    
    # Borrar el mensaje con su id
    def delete(self):
        idMsj = request.json['id']
        try:
            Mensajes.query.filter_by(id=id).delete()
            db.session.commit()
            return {'result': True}
        except:
            db.session.rollback()
            return {"error": "Error al borrar el mensaje"}, 404
          

# ACTIVACIÓN DE LOS PUNTOS DE ACCESO API   

api.add_resource(ListaUsuariosAPI, '/msgs/api/v1.0/users', endpoint='users')    
api.add_resource(MensajesAPI, '/msgs/api/v1.0/messages', endpoint='messages')    


if __name__ == '__main__':
    app.run(debug=True)