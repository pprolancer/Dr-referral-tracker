from django.test import TestCase
from django.contrib.auth.models import User


class UserAuthTest(TestCase):
    ''' a testcases class for Physician model '''

    def setUp(self):
        ''' setup initial objects '''
        self.default_pass = 'pass1234'
        self.user = User.objects.create_user(username='user1',
                                             password=self.default_pass)

    def test_change_user_does_not_make_inactive(self):
        ''' quantifiedcode: ignore it! '''

        self.assertTrue(self.user.is_active)
        self.user.first_name = 'firstname1'
        self.user.save()
        user = User.objects.get(username=self.user.username)
        self.assertTrue(user.is_active)
        self.user.email = 'sample@email.com'
        self.user.save()
        user = User.objects.get(username=self.user.username)
        self.assertTrue(user.is_active)
