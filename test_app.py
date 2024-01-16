from unittest import TestCase

from app import create_app
from models import db, connect_db, User, Post

app = create_app("blogly_test", testing=True)
connect_db(app)

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# Don't use Flask DebugToolbar when testing
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

with app.app_context():
    db.drop_all()
    db.create_all()


class BloglyViewsTests(TestCase):
    """Tests for views for Users."""

    def setUp(self):

        with app.app_context():
            
            # Delete all data in the tables to start fresh.
            User.query.delete()
            Post.query.delete()

            user1 = User(first_name="User", last_name="One", image_url="https://images.unsplash.com/photo-1620336655052-b57986f5a26a")
            user2 = User(first_name="User", last_name="Two")

            db.session.add_all([user1, user2])
            db.session.commit()

            p1 = Post(title='Post 1', content='Content 1 ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', user_id=user1.id)
            p2 = Post(title='Post 2', content='Content 2 ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', user_id=user1.id)
            p3 = Post(title='Post 3', content='Content 3 ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', user_id=user2.id)
            p4 = Post(title='Post 4', content='Content 4 ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', user_id=user2.id)

            db.session.add_all([p1, p2, p3, p4])
            db.session.commit()

            self.user1 = User.query.filter_by(first_name="User", last_name="One").first()
            self.user2 = User.query.filter_by(first_name="User", last_name="Two").first()
            self.post1 = Post.query.filter_by(title="Post 1").first()


    def tearDown(self):
        """Clean up any fouled transaction."""

        with app.app_context():
            db.session.rollback()

    def test_home(self):
    
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Recent Posts</h1>', html)
    
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

    def test_show_create_post_form(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user1.id}/posts/new", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<h1>Add Post for {self.user1.full_name}</h1>', html)

    def test_create_post(self):
        with app.test_client() as client:
            d = {"title": "New Post", "content": "New Content"}
            resp = client.post(f"/users/{self.user1.id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            new_post = Post.query.filter_by(title='New Post').one()

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<a href="/posts/{new_post.id}">New Post</a>', html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post1.id}")
            html = resp.get_data(as_text=True)

            author = User.query.filter_by(id=self.post1.user_id).first()

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<h1>{self.post1.title}</h1>', html)
            self.assertIn(f'By <a href="/users/{author.id}">{author.full_name}</a>', html) 
            
    def test_show_edit_post_form(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post1.id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<h1>Edit Post</h1>', html)
            self.assertIn(f'value="{self.post1.title}"', html)

    def test_edit_post(self):
        with app.test_client() as client:
            d = {"title": "Edited Post", "content": "Edited Content"}
            resp = client.post(f"/posts/{self.post1.id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            edited_post = Post.query.filter_by(title='Edited Post').one()

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<h1>{edited_post.title}</h1>', html)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post1.id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'Post deleted!', html)
            self.assertNotIn(f'{self.post1.title}', html) 


    
