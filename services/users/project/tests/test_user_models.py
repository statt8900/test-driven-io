# External imports
from sqlalchemy.exc import IntegrityError  # type: ignore
# Internal Imports
from project import db
from project.tests.base import BaseTestCase
from project.api.models import User
from project.tests.utils import add_user
# ######################
# # Helper Functions
# # --------------------


class TestUsersDBService(BaseTestCase):
    """test the models.py file"""

    def test_add_user(self) -> None:
        user = add_user(
            username="test",
            email="test@test.com",
            password="password"
        )
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.active)
        self.assertFalse(user.admin)
        self.assertTrue(user.password)

    def test_add_user_duplicate_username(self) -> None:
        """Tests the unique username"""
        add_user(
            username="test",
            email="test@test.com",
            password="password"
        )
        dup_user = User(
            username="test",
            email="newtest@test.com",
            password="password"
        )
        db.session.add(dup_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self) -> None:
        """Tests the unique email"""
        add_user(
            username="test",
            email="test@test.com",
            password="password"
        )
        dup_user = User(
            username="newtest",
            email="test@test.com",
            password="password"
        )
        db.session.add(dup_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_passwords_are_random(self) -> None:
        """Make sure the hash is working"""
        user_one = add_user('test', 'test@test.com', 'password')
        user_two = add_user('test2', 'test2@test.com', 'password')
        self.assertNotEqual(user_one.password, user_two.password)

    def test_to_json(self) -> None:
        """tests to_json method of User"""
        user = add_user(
            username='justatest',
            email='test@test.com',
            password="password"
        )
        self.assertTrue(isinstance(user.to_json(), dict))
