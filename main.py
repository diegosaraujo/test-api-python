# from src.controllers.users import *

from flask import Flask, jsonify, Response, request
from flask_restx import Resource, Api, Namespace
from src.models.user import user
import json

from flask_sqlalchemy import SQLAlchemy
# from src.config.swagger import swagger

app = Flask(__name__)
api = Api(app, version='1.0', title='API from Test PTF', description='API maked from test. Maked by Diego Santos Araujo', doc='/docs')

#app, api = swagger.app, swagger.api
#conn = database.app


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://zosfbmzyjwqbce:8b4318a1bfa2ab78437ec6f254d894c1dc57478abc9f733fe2a436e9cc705f9b@ec2-34-205-46-149.compute-1.amazonaws.com:5432/d20ajc6qfp2q7b'

db = SQLAlchemy(app)#api

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    country = db.Column(db.String(50))

    def to_json(self):
        return {"id": self.id, "name": self.name, "country": self.country}

@api.route('/users',methods=['GET'], defaults={"page": 1, "per_page": 100})
@api.route('/users/<int:page>/<int:per_page>', methods=['GET'])

class UserList(Resource):
    def get(self, page, per_page):
        page = page
        per_page = per_page
        user_database = User.query.order_by(User.id).paginate(page=page, per_page = per_page)

        return generateResponseWithMeta(user_database, True)
        


@api.route('/user/name/<name>', defaults={"page": 1, "per_page": 100})
@api.route('/user/name/<name>/<int:page>/<int:per_page>', methods=['GET'])
class UserByName(Resource):
    def get(self, name, page, per_page):
        page = page
        per_page = per_page
        user_database = User.query.filter(User.name==name.upper()).paginate(page=page, per_page = per_page)
        
        return generateResponseWithMeta(user_database, True)
    

@api.route('/user/country/<name>', defaults={"page": 1, "per_page": 100})
@api.route('/user/country/<name>/<int:page>/<int:per_page>', methods=['GET'])
class UserByCountry(Resource):
    def get(self, name, page, per_page):
        page = page
        per_page = per_page
        user_database = User.query.filter(User.country == name.upper()).paginate(page=page, per_page = per_page)
        
        return generateResponseWithMeta(user_database, True)
    
    
@api.route('/user/id/<id>')
@api.doc(params={'id': 'Id of User'})
class UserById(Resource):
    def get(self, id):
        user_database = User.query.filter(User.id == id)
        
        user_json = [user.to_json() for user in user_database]
        
        response = generateResponse(user_json, True)
        
        return response
    
    

def generateResponseWithMeta(result, success):
    
    data=[]
    
    for user in result.items:
        data.append({
            'id': user.id,
            'name': user.name,
            'country': user.country
        })

        meta = {
            'page': result.page,
            'total_pages': result.pages,
            'total_count': result.total,
            'prev_page': result.prev_num,
            'next_page': result.next_num,
            'has_next': result.has_next,
            'has_prev': result.has_prev,
            'total_items': len(data)
        }
        
    return jsonify({
            'results':data,
            'success': success,
            'meta': meta
        })
    

def generateResponse(result, success):
    return jsonify({
            'results':result,
            'success': success,
        })

app.run()