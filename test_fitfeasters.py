import unittest
from flask import session
from app import app, db
from models import User

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test environment."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        """Tear down test environment."""
        db.session.remove()
        db.drop_all()

    def test_signup(self):
        """Test user signup functionality."""
        response = self.client.post('/signup', data={
            'username': 'testuser',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'image_url': 'https://example.com/test.jpg'
        }, follow_redirects=True)
        self.assertIn(b'Hello, testuser!', response.data)

    def test_login(self):
        """Test user login functionality."""
        # Create a test user
        test_user = User(
            username='testuser',
            password=User.hash_password('testpassword'),
            first_name='Test',
            last_name='User',
            email='test@example.com',
            image_url='https://example.com/test.jpg'
        )
        db.session.add(test_user)
        db.session.commit()

        # Attempt to log in as the test user
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)
        self.assertIn(b'Hello, testuser!', response.data)

    def test_edit_profile(self):
        """Test user profile editing functionality."""
        # Create a test user
        test_user = User(
            username='testuser',
            password=User.hash_password('testpassword'),
            first_name='Test',
            last_name='User',
            email='test@example.com',
            image_url='https://example.com/test.jpg'
        )
        db.session.add(test_user)
        db.session.commit()

        # Log in as the test user
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = test_user.id
        response = c.post('/user/edit_user.html', data={
            'username': 'newusername',
            'email': 'newemail@example.com',
            'password': 'testpassword'
        }, follow_redirects=True)
        self.assertIn(b'Profile updated successfully', response.data)

if __name__ == '__main__':
    unittest.main()