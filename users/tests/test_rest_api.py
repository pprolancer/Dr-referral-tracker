from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class LoginBaseTest(APITestCase):
    ''' a base class for rest testcases which need login '''

    def setUp(self):
        '''initial default user to be login in '''
        self.default_pass = 'pass1234'
        self.user = User.objects.create_superuser(username='user1',
                                                  email='user1@email.com',
                                                  password=self.default_pass)

    def _login(self):
        ''' do login on client '''

        return self.client.login(username=self.user.username,
                                 password=self.default_pass)


class SessionTest(LoginBaseTest):
    ''' testcases class for Session Rest api '''

    def test_login(self):
        ''' login api test '''
        url = reverse('rest_api:session-list')
        data = {'username': self.user.username, 'password': self.default_pass}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.id)

    def test_login_fail(self):
        ''' login api test fail '''
        url = reverse('rest_api:session-list')
        data = {'username': self.user.username, 'password': 'Invalid'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_inactive_user(self):
        ''' login api test inactive user '''
        url = reverse('rest_api:session-list')

        inactive_user = User.objects.create_superuser(
            username='inactive_user', email='inactive_user@email.com',
            password=self.default_pass)
        inactive_user.is_active = False
        inactive_user.save()

        data = {'username': inactive_user.username,
                'password': self.default_pass}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get(self):
        ''' get session api test '''

        self._login()
        url = reverse('rest_api:session-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.id)

    def test_get_not_authorized(self):
        ''' call get api while not authorized '''

        url = reverse('rest_api:session-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout(self):
        ''' logout api test '''

        self._login()
        self.assertEqual(self.client.session.get('_auth_user_id'),
                         str(self.user.id))
        url = reverse('rest_api:session-list')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertIsNone(self.client.session.get('_auth_user_id'))

    def test_logout_not_authorized(self):
        ''' call logout api while not authorized '''

        url = reverse('rest_api:session-list')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
