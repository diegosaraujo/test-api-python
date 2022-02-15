from flask import Flask

class Instance():
    def __init__(self, ):
        self.app = Flask(__name__)
        
        
    def run(self, ):
        self.app.run()
                       
instance = Instance()