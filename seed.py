"""Seed file to make sample data for Blogly db."""

from models import User, db
from app import app

# Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

    # If table isn't empty, empty it
    User.query.delete()

    # Add users
    condor = User(first_name='Condor', last_name='Smith', image_url="https://images.unsplash.com/photo-1620336655052-b57986f5a26a?q=80&w=250")
    phil = User(first_name='Phil', last_name='Rands', image_url="https://images.unsplash.com/photo-1561948955-570b270e7c36?q=80&w=250")
    rachel = User(first_name='Rachel', last_name='Cretin', image_url="https://images.unsplash.com/photo-1630207831419-3532bcb828d7?q=80&w=250")

    db.session.add(condor)
    db.session.add(phil)
    db.session.add(rachel)

    db.session.commit()
