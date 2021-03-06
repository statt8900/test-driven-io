# External imports
import json
import unittest
# Internal Imports
from flask import current_app
from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user
# ######################
# # Helper Functions
# # --------------------


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""
    def login_user(self, email:str,password:str)->str:
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data = json.dumps({'email':'test@test.com','password':'test'}),
                content_type='application/json'
            )
            auth_token = json.loads(resp_login.data.decode())['auth_token']
        return auth_token

    def set_admin(self,email : str)->None:
        user = User.query.filter_by(email=email).first()
        user.admin = True
        db.session.commit()

    def test_users(self) -> None:
        """Ensure the /ping route behaves correctly."""
        response = self.client.get("/users/ping")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("pong!", data["message"])
        self.assertIn("success", data["status"])

    def test_add_user(self) -> None:
        """ensure adding a user works correctly"""
        add_user('test','test@test.com','test')
        self.set_admin('test@test.com')
        auth_token = self.login_user('test@test.com','test')
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps(
                    {"username": "michael",
                     "email": "michael@mherman.org",
                     "password": "test"}
                ),
                content_type="application/json",
                headers={'Authorization':f'Bearer {auth_token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn("michael@mherman.org was added!", data["message"])
            self.assertIn("success", data["status"])

    def test_add_user_invalid_json(self) -> None:
        add_user('test','test@test.com','test')
        self.set_admin('test@test.com')
        auth_token = self.login_user('test@test.com','test')
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({}),
                content_type="application/json",
                headers={'Authorization':f'Bearer {auth_token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_invalid_json_no_password(self) -> None:
        add_user('test','test@test.com','test')
        self.set_admin('test@test.com')
        auth_token = self.login_user('test@test.com','test')
        with self.client:
            payload = {'username': 'test999', 'email': 'test999@test.com'}
            response = self.client.post(
                "/users",
                data=json.dumps(payload),
                content_type="application/json",
                headers={'Authorization':f'Bearer {auth_token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_invalid_inactive(self) -> None:
        add_user('test','test@test.com','test')
        self.set_admin('test@test.com')
        # inactivate user
        user = User.query.filter_by(email='test@test.com').first()
        user.active = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data = json.dumps({'email':'test@test.com','password':'test'}),
                content_type='application/json'
            )
            auth_token = json.loads(resp_login.data.decode())['auth_token']
            payload = {
                'username':'mike',
                'email':'mike@mike.com',
                'password':'test'
            }
            response = self.client.post(
                "/users",
                data=json.dumps(payload),
                headers={'Authorization':f'Bearer {auth_token}'},
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertIn('Provide a valid auth token.', data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_invalid_inactive(self) -> None:
        add_user('test','test@test.com','test')
        user = User.query.filter_by(email='test@test.com').first()
        user.active = False
        db.session.commit()
        self.set_admin('test@test.com')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data = json.dumps({'email':'test@test.com','password':'test'}),
                content_type='application/json'
            )
            auth_token = json.loads(resp_login.data.decode())['auth_token']
            payload = {
                'username':'mike',
                'email':'mike@mike.com',
                'password':'test'
            }
            response = self.client.post(
                "/users",
                data=json.dumps(payload),
                headers={'Authorization':f'Bearer {auth_token}'},
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertIn('Provide a valid auth token.', data["message"])
            self.assertEqual(response.status_code, 401)
            self.assertIn("fail", data["status"])

    def test_add_user_duplicate_user(self) -> None:
        add_user('test','test@test.com','test')
        self.set_admin('test@test.com')
        auth_token = self.login_user('test@test.com','test')
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps(
                    {"username": "michael",
                     "email": "michael@mherman.org",
                     "password": "password"}
                ),
                content_type="application/json",
                headers={'Authorization':f'Bearer {auth_token}'},
            )
            response = self.client.post(
                "/users",
                data=json.dumps(
                    {"username": "michael",
                     "email": "michael@mherman.org",
                     "password": "password"}
                ),
                content_type="application/json",
                headers={'Authorization':f'Bearer {auth_token}'},
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("michael@mherman.org already in database",
                          data["message"])
            self.assertIn("fail", data["status"])

    def test_get_user(self) -> None:
        user = add_user("michael", "michael@mherman.org", "password")
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.get(f"/users/{user.id}")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("michael@mherman.org", data["data"]["email"])
            self.assertIn("michael", data["data"]["username"])
            self.assertIn("success", data["status"])

    def test_get_user_no_id(self) -> None:
        with self.client:
            response = self.client.get("/users/999")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("fail", data["status"])
            self.assertIn("User does not exist", data["message"])

    def test_all_users(self) -> None:
        add_user("test", "test@test.com", "test")
        auth_token = self.login_user('test@test.com','test')
        self.set_admin('test@test.com')
        add_user("test2", "test2@test.com", "password")
        with self.client:
            response = self.client.get(
                "/users",
                headers={'Authorization':f'Bearer {auth_token}'},
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("test@test.com", data["data"]["users"][0]["email"])
            self.assertIn("test", data["data"]["users"][0]["username"])
            self.assertIn("test2@test.com", data["data"]["users"][1]["email"])
            self.assertIn("test2", data["data"]["users"][1]["username"])
            self.assertIn("success", data["status"])
            self.assertTrue(data['data']['users'][0]['admin'])
            self.assertFalse(data['data']['users'][1]['admin'])

    def test_main_no_users(self) -> None:
        """Ensure the main route behaves correctly when no users have been
        added to the database."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"All Users", response.data)
        self.assertIn(b"<p>No users!</p>", response.data)

    def test_main_with_users(self) -> None:
        """Ensure the main route behaves correctly when users have been
        added to the database."""
        add_user("michael", "michael@mherman.org", "password")
        add_user("fletcher", "fletcher@notreal.com", "password")
        with self.client:
            response = self.client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"All Users", response.data)
            self.assertNotIn(b"<p>No users!</p>", response.data)
            self.assertIn(b"michael", response.data)
            self.assertIn(b"fletcher", response.data)

    def test_main_add_user(self) -> None:
        """
        Ensure a new user can be added to the database via a POST request.
        """
        with self.client:
            response = self.client.post(
                "/",
                data=dict(username="michael",
                          email="michael@sonotreal.com", password="password"),
                follow_redirects=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"All Users", response.data)
            self.assertNotIn(b"<p>No users!</p>", response.data)
            self.assertIn(b"michael", response.data)

    def test_encode_auth_token(self) -> None:
        user = add_user('justatest', 'test@test.com', 'test')
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self) -> None:
        user = add_user('justatest', 'test@test.com', 'test')
        auth_token = user.encode_auth_token(user.id)
        self.assertEqual(user.id, user.decode_auth_token(auth_token))

    def test_expired_auth_token(self) -> None:
        user = add_user('justatest', 'test@test.com', 'test')
        current_app.config['TOKEN_EXPIRATION_SECONDS'] = -1
        auth_token = user.encode_auth_token(user.id)
        self.assertIn('Signature expired. Please log in again.',
                      user.decode_auth_token(auth_token))


if __name__ == "__main__":
    unittest.main()
