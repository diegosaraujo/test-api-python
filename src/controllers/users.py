from flask import Flask, jsonify, Response, request
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



@api.route('/users',methods=['GET'], defaults={"page": 1, "per_page": 100})
@api.route('/users/<int:page>/<int:per_page>', methods=['GET'])

@api.doc(params={'page': 'Page of pagination', 'per_page': 'Total items returned in pagination'})

class UserList(Resource):
    #@api.marshal_list_with(user)
    def get(self, page, per_page):
        page = page
        per_page = per_page
        user_database = User.query.order_by(User.id).paginate(page=page, per_page = per_page)

        data=[]
        for user in user_database.items:
            data.append({
                'id': user.id,
                'name': user.name,
                'country': user.country
            })

        
        meta = {
            'page': user_database.page,
            'total_per_pages': len(data),
            'total_count': user_database.total,
            'prev_page': user_database.prev_num,
            'next_page': user_database.next_num,
            'has_next': user_database.has_next,
            'has_prev': user_database.has_prev
        }
        
        return jsonify({
            'results':data,
            'success': True,
            'meta': meta
        })


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