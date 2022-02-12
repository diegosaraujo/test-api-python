from flask import Flask
from flask_restx import Api

class Swagger():
    def __init__(self, ):
        self.app = Flask(__name__)
        
        self.api = Api(self.app, version='1.0', 
                       title='API from Test PTF',
                       description='API maked from test. Maked by Diego Santos Araujo',
                       doc='/docs'            
                       )
        
    def run(self, ):
        self.app.run()
            
            
swagger = Swagger()