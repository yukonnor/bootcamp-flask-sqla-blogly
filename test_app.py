from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# Don't use Flask DebugToolbar when testing
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

with app.test_request_context():
    db.drop_all()
    db.create_all()


class BloglyViewsTests(TestCase):
    """Tests for views for Users."""

    def setUp(self):

        with app.test_request_context():

            # DEBGUGGING
            print(f"SQLALCHEMY_DATABASE_URI (before): {app.config['SQLALCHEMY_DATABASE_URI']}")
            print(f"SQLALCHEMY_ECHO (before): {app.config['SQLALCHEMY_ECHO']}")
            
            # Delete all data in the users table to start fresh.
            User.query.delete()

            user1 = User(first_name="User", last_name="One", image_url="https://images.unsplash.com/photo-1620336655052-b57986f5a26a")
            user2 = User(first_name="User", last_name="Two")

            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

            self.user1 = user1
            self.user2 = user2

            # DEBGUGGING
            print(f"SQLALCHEMY_DATABASE_URI (after): {app.config['SQLALCHEMY_DATABASE_URI']}")
            print(f"SQLALCHEMY_ECHO (after): {app.config['SQLALCHEMY_ECHO']}")

    def tearDown(self):
        """Clean up any fouled transaction."""

        with app.test_request_context():
            db.session.rollback()

    def test_home(self):
    
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)
    
    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_show_create_user_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create User</h1>', html)

    def test_create_user(self):
        with app.test_client() as client:
            d = {"first_name": "Created", "last_name": "Viaform", "image_url": ""}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            user3 = User.query.filter_by(first_name='Created').one()

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<a href="/users/{user3.id}">Created Viaform</a>', html) 

    def test_show_user_detail_page(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user1.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>User One</h1>', html)
            self.assertIn(self.user1.image_url, html)

    def test_show_user_detail_page_default_img(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user2.id}")
            html = resp.get_data(as_text=True)

            default_image_url = User.get_default_image()

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>User Two</h1>', html)
            self.assertIn(default_image_url, html)

    def test_show_edit_user_form(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user1.id}/edit", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Edit User</h1>', html)

    def test_edit_user(self):
        with app.test_client() as client:
            d = {"first_name": "Edited", "last_name": "Viaform", "image_url": ""}
            resp = client.post(f"/users/{self.user1.id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<a href="/users/{self.user1.id}">Edited Viaform</a>', html) 

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user1.id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(f'<a href="/users/{self.user1.id}">{self.user1.first_name} {self.user1.last_name}</a>', html) 
            

    
