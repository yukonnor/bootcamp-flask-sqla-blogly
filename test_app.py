from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class BloglyViewsTests(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample pet."""

        # Delete all data in the pets table to start fresh.
        User.query.delete()

        user1 = User(first_name="User", last_name="One", image_url="https://images.unsplash.com/photo-1620336655052-b57986f5a26a?q=80&w=250")
        user2 = User(first_name="User", last_name="Two")

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        self.user1_id = user1.id
        self.user2_id = user2.id
        self.user1 = user1
        self.user2 = user2

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_home(self):
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)
    
    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_show_create_user_form(self):
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create User</h1>', html)

    def test_create_user(self):
        with app.test_client() as client:
            d = {"first_name": "Created", "last_name": "Viaform"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<a href="/users/3">Created Viaform</a>', html) # Note: probably best to avoid hard coding "3" here

    def test_show_user_detail_page(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user1_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>User One</h1>', html)
            self.assertIn('https://images.unsplash.com/photo-1620336655052-b57986f5a26a?q=80&w=250', html)
            

    
