import unittest
from shanbay import create_app, db
from shanbay.models import User


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        user = User(password='password')
        self.assertTrue(user.password_hash is not None)

    def test_password_getter(self):
        user = User(password='password')
        with self.assertRaises(AttributeError):
            user.password

    def test_password_random_salt(self):
        user1 = User(password='password')
        user2 = User(password='password')
        self.assertNotEqual(user1.password_hash, user2.password_hash)

    def test_password_validate(self):
        user = User(password='password')
        self.assertTrue(user.verify_password('password'))

