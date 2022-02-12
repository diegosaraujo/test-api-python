from flask import Flask
from flask_restx import Resource, Api, Namespace
from src.models.user import user

from src.config.swagger import swagger

app, api = swagger.app, swagger.api


# Depois terá que vir do banco de dados
users_db = [
    {'id':1, 'name': 'Diego', 'country':'Brazil'}, 
    {'id':2, 'name': 'Thabata', 'country':'Argentina'}
    ]

@api.route('/users')
class UserList(Resource):
    @api.marshal_list_with(user)
    def get(self, ):
        return users_db
