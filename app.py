from src.config.instance import instance
from flask_sqlalchemy import SQLAlchemy
import src.controllers.user_controller
app, api =  instance.app, instance.api

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)