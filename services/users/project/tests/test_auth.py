# Typing imports

# External imports
import json
from flask import current_app
# Internal Imports
from project.tests.base import BaseTestCase
from project.tests.utils import add_user
from project import db
from project.api.models import User


class TestAuthBlueprint(BaseTestCase):

    def test_user_registration(self) -> None:
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'michael',
                    'email': 'michael@test.com',
                    'password': 'password',
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_user_registration_duplicate_email(self) -> None:
        userdata = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'password'
        }
        add_user(**userdata)
        userdata['username'] = 'test2'
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(userdata),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] ==
                            'Sorry. That user already exists.')
            self.assertEqual(response.status_code, 400)

    def test_user_registration_duplicate_username(self) -> None:
        userdata = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'password'
        }
        add_user(**userdata)
        userdata['email'] = 'test2@test.com'
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(userdata),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] ==
                            'Sorry. That user already exists.')
            self.assertEqual(response.status_code, 400)

    def test_user_registration_invalid_payload(self) -> None:
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] ==
                            'Invalid payload.')
            self.assertEqual(response.status_code, 400)

    def test_registered_user_login(self) -> None:
        userdata = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'password'
        }
        add_user(**userdata)
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps(
                    {'email': 'test@test.com', 'password': 'password'}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'],
                             'Successfully logged in.')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

    def test_unregistered_user_login(self) -> None:
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps(
                    {'email': 'test@test.com', 'password': 'password'}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertEqual(data['message'],
                             'User does not exist.')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.content_type, 'application/json')

    def test_valid_logout(self) -> None:
        userdata = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'password'
        }
        add_user(**userdata)
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps(
                    {'email': 'test@test.com', 'password': 'password'}),
                content_type='application/json'
            )
            token = json.loads(response.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'], 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)

    def test_invalid_logout_expired_token(self) -> None:
        userdata = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'password'
        }
        current_app.config['TOKEN_EXPIRATION_SECONDS'] = -1
        add_user(**userdata)
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps(
                    {'email': 'test@test.com', 'password': 'password'}),
                content_type='application/json'
            )
            token = json.loads(response.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(
                data['message'], 'Signature expired. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_invalid_logout_inactive_user(self) -> None:
        userdata = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'password'
        }
        add_user(**userdata)
        user = User.query.filter_by(email=userdata['email']).first()
        user.active = False
        db.session.commit()
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps(
                    {'email': 'test@test.com', 'password': 'password'}),
                content_type='application/json'
            )
            token = json.loads(response.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(
                data['message'], 'Provide a valid auth token.')
            self.assertEqual(response.status_code, 401)

    def test_invalid_logout_no_token(self) -> None:
        with self.client:
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': 'Bearer Invalid'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(
                data['message'], 'Invalid token. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_status_valid(self) -> None:
        userdata = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'password'
        }
        add_user(**userdata)
        user = User.query.filter_by(email='test@test.com').first()
        user.admin = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(
                    {'email': 'test@test.com', 'password': 'password'}),
                content_type='application/json'
            )
            auth_token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/status',
                headers={'Authorization': f'Bearer {auth_token}'},
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'success')
            self.assertNotEqual(data['data'], None)
            self.assertEqual(data['data']['username'], 'test')
            self.assertEqual(data['data']['email'], 'test@test.com')
            self.assertTrue(data['data']['active'])
            self.assertFalse(data['data']['admin'])
            self.assertEqual(response.status_code, 200)

    def test_status_invalid_inactive_user(self) -> None:
        userdata = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'password'
        }
        add_user(**userdata)
        user = User.query.filter_by(email=userdata['email']).first()
        user.active = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(
                    {'email': 'test@test.com', 'password': 'password'}),
                content_type='application/json'
            )
            auth_token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/status',
                headers={'Authorization': f'Bearer {auth_token}'},
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(
                data['message'], 'Provide a valid auth token.')
            self.assertEqual(response.status_code, 401)

    def test_status_invalid(self) -> None:
        with self.client:
            response = self.client.get(
                '/auth/status',
                headers={'Authorization': f'Bearer Invalid'},
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(
                data['message'], 'Invalid token. Please log in again.')
            self.assertEqual(response.status_code, 401)
