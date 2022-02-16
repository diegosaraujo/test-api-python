from flask import Flask
from flask_restx import Api

class Instance():
    def __init__(self, ):
        self.app = Flask(__name__)
        self.api = Api(self.app, version='1.0', title='API from Test PTF', description='API maked from test. Maked by Diego Santos Araujo', doc='/docs', default='UserController', default_label='This controller return datas of User')
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://zosfbmzyjwqbce:8b4318a1bfa2ab78437ec6f254d894c1dc57478abc9f733fe2a436e9cc705f9b@ec2-34-205-46-149.compute-1.amazonaws.com:5432/d20ajc6qfp2q7b'

    def run(self, ):
        self.app.run()
                       
instance = Instance()