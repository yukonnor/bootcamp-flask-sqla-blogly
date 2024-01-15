"""Seed file to make sample data for Blogly db."""

from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

    # If table isn't empty, empty it
    User.query.delete()
    Post.query.delete()

    # Add users
    condor = User(first_name='Condor', last_name='Smith', image_url="https://images.unsplash.com/photo-1620336655052-b57986f5a26a")
    phil = User(first_name='Phil', last_name='Rands', image_url="https://images.unsplash.com/photo-1561948955-570b270e7c36")
    rachel = User(first_name='Rachel', last_name='Chrisy', image_url="https://images.unsplash.com/photo-1630207831419-3532bcb828d7")

    # Add posts
    p1 = Post(title='A New World', content='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', user_id=1)
    p2 = Post(title='City Streets', content='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', user_id=1)
    p3 = Post(title='A Future of Robotaxis', content='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', user_id=2)
    p4 = Post(title='Growing Grass Turf', content='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', user_id=2)
    p5 = Post(title='Thoughts on Corn', content='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', user_id=3)
    p6 = Post(title='10 Reasons Pigs Rule', content='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', user_id=3)

    db.session.add_all([condor, phil, rachel, p1, p2, p3, p4, p5, p6])
    db.session.commit()

    # Add post tags
    t1 = Tag(name='City Planning', 
             tag_posts=[PostTag(post_id=1),
                        PostTag(post_id=2),
                        PostTag(post_id=3)])
    t2 = Tag(name='Agriculture',
             tag_posts=[PostTag(post_id=1),
                        PostTag(post_id=4),
                        PostTag(post_id=5)])

    db.session.add_all([t1, t2])
    db.session.commit()
