"""Models for the Blogle app"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50),  # string with max len of 50 chars
                     nullable=False,
                     unique=True)
    
    last_name = db.Column(db.String(50),  # string with max len of 50 chars
                     nullable=False,
                     unique=True)

    image_url = db.Column(db.String(200), nullable=False, default="https://st3.depositphotos.com/6672868/13701/v/450/depositphotos_137014128-stock-illustration-user-profile-icon.jpg")

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


                     


