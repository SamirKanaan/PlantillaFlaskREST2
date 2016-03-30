# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 19:35:19 2016

@author: samir
"""

# Creación de RESTful API con Flask+RESTful extension
# Solo añadir/ver/eliminar usuarios en un diccionario en memoria
# a modo de ejemplo sencillo

from flask import Flask, jsonify, abort
from flask.ext.restful import Api, Resource

app = Flask(__name__)
api = Api(app)


# Aquí se guardarán los usuarios: {id: correo}
usuarios = {}


# Forma sencilla: mejor trabajar con reqparse
from flask import request

class UserListAPI(Resource):
    def get(self):
        return usuarios
    
    def put(self):
        pass
    
    def post(self):
        nuevoId = len(usuarios)
        usuarios[nuevoId] = request.json['email']
        return request.json
    
    def delete(self):
        idUsuario = request.json['id']
        if idUsuario in usuarios:
            del usuarios[idUsuario]
            return {'result': True}
        else:
            abort(404)
            
    

api.add_resource(UserListAPI, '/msgs/api/v1.0/users', endpoint='users')    


if __name__ == '__main__':
    app.run(debug=True)