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

    image_url = db.Column(db.String(200), nullable=False)

    def __init__(self, first_name, last_name, image_url=None, **kwargs):
        if image_url is None:
            image_url = self.get_default_image()
        super().__init__(first_name=first_name, last_name=last_name, image_url=image_url, **kwargs)

    @classmethod
    def get_default_image(cls):
        default_img_url="https://st3.depositphotos.com/6672868/13701/v/450/depositphotos_137014128-stock-illustration-user-profile-icon.jpg"
        
        return default_img_url
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name}"
    
    def hide_default_image(self):
        if self.image_url == self.get_default_image():
            self.image_url = ""




                     


