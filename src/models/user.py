from flask_restx import fields

from src.config.swagger import swagger

user = swagger.api.model('User', {
    'id': fields.Integer,
    'name': fields.String,
    'country': fields.String
})