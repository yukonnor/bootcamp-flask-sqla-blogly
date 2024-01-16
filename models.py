"""Models for the Blogle app"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50),  # string with max len of 50 chars
                     nullable=False)
    
    last_name = db.Column(db.String(50),  # string with max len of 50 chars
                     nullable=False)

    image_url = db.Column(db.String(200), nullable=False)

    # SQLA relationship to a user's post(s)
    posts = db.relationship('Post', cascade='all, delete-orphan')

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

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(200),  
                    nullable=False)
    
    content = db.Column(db.String(5000),  
                    nullable=False)
    
    created_at = db.Column(db.DateTime,
                    nullable=False,
                    default=datetime.now())

    user_id = db.Column(db.Integer,
                    db.ForeignKey('users.id', ondelete='CASCADE'))
    
    # relationship to a post's user
    user = db.relationship('User')

    # relationship to the post's tags. 
    post_tags = db.relationship('PostTag', backref='posts')

    tags = db.relationship('Tag',
                            secondary='posts_tags')

    @classmethod
    def get_recent_posts(cls, limit=5):
        """Class method to retrieve the 'limit' most recent posts."""
        return cls.query.order_by(cls.created_at.desc()).limit(limit).all()
    
    @property
    def pretty_date(self):
        """Return the post's created at in the format: May 1, 2015, 10:30 AM"""

        pretty_datetime = self.created_at.strftime("%B %d, %Y, %I:%M %p")
        
        return pretty_datetime
    

    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} created_at={p.created_at}"
    
class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.String(50),  
                    nullable=False)
    
    # relationship to the tag's posts. 
    tag_posts = db.relationship('PostTag', backref='tags')

    posts = db.relationship('Post',
                            secondary='posts_tags')

    def __repr__(self):
        t = self
        return f"<Tag id={t.id} name={t.name}"
    

class PostTag(db.Model):
    """Join table for Posts to Tags."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer,
                       db.ForeignKey("posts.id"),
                       primary_key=True)
    
    tag_id = db.Column(db.Integer,
                          db.ForeignKey("tags.id"),
                          primary_key=True)
    
    def __repr__(self):
        pt = self
        return f"<PostTag post_id={pt.post_id} tag_id={pt.tag_id}>"




                     





                     


