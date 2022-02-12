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
        return jsonify({
            'results':user_json, 
            'success': True,
            'count': len(user_database)
            })
