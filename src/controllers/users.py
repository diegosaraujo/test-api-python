from flask import Flask, jsonify, Response
from flask_restx import Resource, Api, Namespace
from src.models.user import user
import json

from flask_sqlalchemy import SQLAlchemy
from src.config.swagger import swagger

app, api = swagger.app, swagger.api
#conn = database.app


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/ptf'

db = SQLAlchemy(app)#api

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    country = db.Column(db.String(50))
    
    def to_json(self):
        return {"id": self.id, "name": self.name, "country": self.country}
        


@api.route('/users')
class UserList(Resource):
    #@api.marshal_list_with(user)
    def get(self, ):
        user_database = User.query.all()
        user_json = [user.to_json() for user in user_database]
        
        response = generateResponse(user_json, True)
        
        return response


@api.route('/user/name/<name>')
@api.doc(params={'name': 'Name of user'})
class UserByName(Resource):
    def get(self, name):
        user_database = User.query.filter(User.name==name.upper())
        
        user_json = [user.to_json() for user in user_database]
        
        response = generateResponse(user_json, True)
        
        return response
    

@api.route('/user/country/<name>')
@api.doc(params={'name': 'Name of country'})
class UserByCountry(Resource):
    def get(self, name):
        user_database = User.query.filter(User.country == name.upper())
        
        user_json = [user.to_json() for user in user_database]
        
        response = generateResponse(user_json, True)
        
        return response
    
    
@api.route('/user/id/<id>')
@api.doc(params={'id': 'Id of User'})
class UserById(Resource):
    def get(self, id):
        user_database = User.query.filter(User.id == id)
        
        user_json = [user.to_json() for user in user_database]
        
        response = generateResponse(user_json, True)
        
        return response
    
    

def generateResponse(result, success):
    return jsonify({
            'results':result,
            'success': success,
            'count': len(result)
        })