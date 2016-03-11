from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class RegisterViewTest(TestCase):
    ''' testcases class for RegisterView '''

    def setUp(self):
        '''initial default user to be login in '''
        pass

    def test_register(self):
        ''' quantifiedcode: ignore it! '''
        default_pass = 'pass1234'
        data = dict(
            username='user1', password=default_pass, password1=default_pass
        )
        response = self.client.post(reverse('user_register'), data)
        self.assertEqual(response.status_code, 302)
        query = User.objects.filter(username=data['username'])
        self.assertEqual(query.count(), 1)
        user = query[0]
        self.assertTrue(user.check_password(default_pass))
        self.assertFalse(user.is_active)

    def test_register_missing_data(self):
        ''' quantifiedcode: ignore it! '''
        data = dict(username='user1')
        response = self.client.post(reverse('user_register'), data)
        self.assertEqual(response.status_code, 200)
        query = User.objects.filter(username=data['username'])
        self.assertEqual(query.count(), 0)
        context = response.context
        form = context['form']
        self.assertIn('password',  form.errors)
        self.assertIn('password1',  form.errors)

    def test_register_no_match_password(self):
        ''' quantifiedcode: ignore it! '''
        data = dict(username='user1', password='pass1234', password1='nomatch')
        response = self.client.post(reverse('user_register'), data)
        self.assertEqual(response.status_code, 200)
        query = User.objects.filter(username=data['username'])
        self.assertEqual(query.count(), 0)
        context = response.context
        form = context['form']
        self.assertIn('password1',  form.errors)

    def test_no_login_redirect(self):
        ''' quantifiedcode: ignore it! '''
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '{}?next={}'.format(
            reverse('user_login'), reverse('index')))
