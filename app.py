"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  =  False
app.config['SQLALCHEMY_ECHO'] =  True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home():
    """If client navigates to root, redirect to users page"""
    
    return redirect('/users')

@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def show_create_user_form():
    """Show a form that can be used to create a user"""

    return render_template('create-user.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    if (image_url):
        new_user  = User(first_name=first_name, last_name=last_name, image_url=image_url)
    else:
        # use default image url if user doesn't provide
        new_user  = User(first_name=first_name, last_name=last_name)
    
    db.session.add(new_user)
    db.session.commit()

    flash(f"New user created!", "success")
    return redirect(f'/users')
