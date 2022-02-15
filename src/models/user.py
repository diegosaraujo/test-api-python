from src.config.instance import instance
from flask_sqlalchemy import SQLAlchemy


app = instance.app

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    country = db.Column(db.String(50))

    def to_json(self):
        return {"id": self.id, "name": self.name, "country": self.country}