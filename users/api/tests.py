from audioop import reverse

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

User = get_user_model()


class AccountTests(APITestCase):
    """User Registrations and Authentications test cases"""

    def test_user_registration(self):
        """
        Ensure we can create a new account object.
        """
        url = '/api-auth/users/'  # Please ignore url hard-coding
        data = {'username': 'testUser', 'password': 'some_strong_pas2',
                'email': 'test@test.com'}
        response_data = {'id': 1, 'username': 'testUser',
                         'email': 'test@test.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, response_data)
        self.assertEqual(User.objects.get(id=1).username, 'testUser')

    def test_user_registration_without_username(self):
        """
        Ensure we can't create a new account without username.
        """
        url = '/api-auth/users/'
        data = {'email': 'test@test.com', 'password': 'some_strong_pas2'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_jwt_authentication(self):
        """Testing user authentication and user access."""
        url = '/api-auth/jwt/create'
        user = User.objects.create_user(username='user', email='user@foo.com',
                                        password='pass')
        user.is_active = False
        user.save()

        response = self.client.post(url, {'email': 'user@foo.com',
                                          'password': 'pass'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        response = self.client.post(url, {'username': 'user',
                                          'password': 'pass'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)

        access_token = response.data['access']

        verification_url = '/api-auth/jwt/verify'
        response = self.client.post(verification_url, {'token': access_token},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(verification_url, {'token': 'abc'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + 'abc')
        response = self.client.get('/api-auth/users/me/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + access_token)
        response = self.client.get('/api-auth/users/me/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
