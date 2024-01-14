"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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
    """Blogly's home page. Shows the 5 latest posts."""

    recent_posts = Post.get_recent_posts()
    
    return render_template('home.html', posts=recent_posts)

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

@app.route('/users/<int:user_id>')
def show_user_detail_page(user_id):
    """Show a page that includes details about a specific user. 
       THe page also has an edit button and a delete button to perform actions on the user."""
     
    user = User.query.get_or_404(user_id)

    return render_template("user-details.html", user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    """Show a form that can be used to edit and existing a user"""

    user = User.query.get_or_404(user_id)

    user.hide_default_image()

    return render_template('edit-user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    user = User.query.get_or_404(user_id)

    user.first_name = first_name
    user.last_name = last_name
    
    if (image_url):
        user.image_url = image_url
    else:
        # use default image url if user doesn't provide
        user.image_url = User.get_default_image()
    
    try: 
        # db.session.add(user) # don't think session.add() is necessary
        db.session.commit()
    except:
        db.session.rollback()
        flash(f"Something went wrong :/", "warning")

    flash(f"User updated!", "success")
    return redirect(f'/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):

    user_to_delete = User.query.get_or_404(user_id)

    try: 
        db.session.delete(user_to_delete)
        db.session.commit()
        flash(f"User deleted!", "success")
    except:
        db.session.rollback()
        flash(f"Something went wrong :/", "warning")

    return redirect(f'/users')

@app.route('/users/<int:user_id>/posts/new')
def show_create_post_form(user_id):
    """Show a form that can be used to create a new post for a user"""

    user = User.query.get_or_404(user_id)

    return render_template('create-post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def create_post(user_id):
    """Process the create post form submission."""
    title = request.form["title"]
    content = request.form["content"]

    new_post  = Post(title=title, content=content, user_id=user_id)
    
    try: 
        db.session.add(new_post)
        db.session.commit()

        flash(f"New post created!", "success")
    except:
        db.session.rollback()
        flash(f"Something went wrong :/", "warning")

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post page"""

    post = Post.query.get_or_404(post_id)

    return render_template('post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Show a form that can be used to edit a user's post"""

    post = Post.query.get_or_404(post_id)

    return render_template('edit-post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Process the edit post form submission"""

    title = request.form["title"]
    content = request.form["content"]

    post = Post.query.get_or_404(post_id)

    post.title = title
    post.content = content
    
    try: 
        # db.session.add(post) # don't think session.add() is necessary
        db.session.commit()

        flash(f"Post updated!", "success")
    except:
        db.session.rollback()
        flash(f"Something went wrong :/", "warning")

    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):

    post_to_delete = Post.query.get_or_404(post_id)
    author_id = post_to_delete.user.id

    db.session.delete(post_to_delete)
    
    try: 
        db.session.commit()
        flash(f"Post deleted!", "success")
    except:
        db.session.rollback()
        flash(f"Something went wrong :/", "warning")

    return redirect(f'/users/{author_id}')