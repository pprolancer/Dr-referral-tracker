from datetime import datetime, timedelta
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from tracking.models import Organization, Physician, Referral


def date2str(d):
    return d.strftime('%Y-%m-%d %H:%M:%S')


class LoginBaseTest(TestCase):
    def setUp(self):
        self.default_pass = 'pass1234'
        self.user = User.objects.create_user(username='user1',
                                             password=self.default_pass)

    def login(self):
        return self.client.post(reverse('user_login'),
                                {'username': self.user.username,
                                 'password': self.default_pass})


class IndexViewTest(LoginBaseTest):
    def test_no_login_get(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)

    def test_get(self):
        self.login()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        today = datetime.today().date()
        context = response.context
        self.assertEqual(len(context["physician_visit_sum"]), 0)
        self.assertEqual(len(context["org_visit_sum"]), 0)
        self.assertEqual(len(context["special_visit_sum"]), 0)
        self.assertEqual(len(context["referrals"]), 0)
        self.assertEqual(len(context["all_orgs"]), 0)
        self.assertEqual(context['today'], today)
        self.assertEqual(context['week_ago'], today - timedelta(days=7))

    def test_post_phyform(self):
        org = Organization.objects.create(org_name='org1')
        self.login()
        data = {
            'phyform': 'submit',
            'organization': org.id,
            'physician_name': 'phys1',
            'physician_phone': '+442083661177',
            'physician_email': 'test@email.com',
            'referral_special': 'on'
        }
        response = self.client.post(reverse('index'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        physicians = Physician.objects.all()
        self.assertEqual(len(physicians), 1)
        created_physician = physicians[0]
        self.assertEqual(created_physician.organization, org)
        self.assertEqual(created_physician.physician_name,
                         data['physician_name'])
        self.assertEqual(created_physician.physician_phone,
                         data['physician_phone'])
        self.assertEqual(created_physician.physician_email,
                         data['physician_email'])
        self.assertEqual(created_physician.referral_special, True)

    def test_post_orgform(self):
        self.login()
        data = {
            'orgform': 'submit',
            'org_name': 'org1',
            'org_contact_name': 'contact1',
            'org_phone': '+442083661177',
            'org_email': 'test@email.com',
            'org_special': 'on'
        }
        response = self.client.post(reverse('index'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        organizations = Organization.objects.all()
        self.assertEqual(len(organizations), 1)
        created_org = organizations[0]
        self.assertEqual(created_org.org_name, data['org_name'])
        self.assertEqual(created_org.org_contact_name,
                         data['org_contact_name'])
        self.assertEqual(created_org.org_phone, data['org_phone'])
        self.assertEqual(created_org.org_email, data['org_email'])
        self.assertEqual(created_org.org_special, True)


class LogoutViewTest(LoginBaseTest):
    def test_logout(self):
        self.login()
        response = self.client.get(reverse('index'))
        self.assertEqual(str(self.user.id),
                         self.client.session.get('_auth_user_id'))
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, '/')
        self.assertIsNone(self.client.session.get('_auth_user_id'))


class ReferralViewTest(LoginBaseTest):
    def test_add_get_form(self):
        self.login()
        response = self.client.get(reverse('add-referral'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracking/referral.html')

    def test_add_post_form(self):
        self.login()
        organization = Organization.objects.create(org_name='org1')
        physician = Physician.objects.create(
            physician_name='phys1', organization=organization)
        today = timezone.now()
        data = {
            'physician': physician.id,
            'visit_date': str(today.date()),
            'visit_count': 1,
            'referral_date': str(today)
        }
        response = self.client.post(reverse('add-referral'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('add-referral'))
        referrals = Referral.objects.all()
        self.assertEqual(len(referrals), 1)
        created_ref = referrals[0]
        self.assertEqual(created_ref.physician, physician)
        self.assertEqual(created_ref.visit_count, data['visit_count'])
        self.assertEqual(created_ref.visit_date, today.date())
        self.assertEqual(date2str(created_ref.referral_date),
                         date2str(today))


class GetReferralReportViewTest(LoginBaseTest):
    def test_get(self):
        self.login()
        response = self.client.get(reverse('get-referral-view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracking/show_referral_report.html')


class GetReferralHistoryViewTest(LoginBaseTest):
    def test_get(self):
        self.login()
        response = self.client.get(reverse('referral-history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'tracking/show_referral_history.html')

    def test_post(self):
        organization = Organization.objects.create(org_name='org1')
        physician = Physician.objects.create(
            physician_name='phys1', organization=organization)
        today = datetime.now().date()
        referrals = [
            Referral.objects.create(physician=physician,
                                    visit_date=today + timedelta(days=i))
            for i in range(10)]

        self.login()
        data = {
            'from_date': str(today),
            'to_date': str(today)
        }
        response = self.client.post(reverse('referral-history'), data)
        context = response.context
        self.assertEqual(len(context['referrals']), 1)
        self.assertEqual(context['referrals'][0], referrals[0])

        data = {
            'from_date': str(today),
            'to_date': str(today+timedelta(days=len(referrals)))
        }
        response = self.client.post(reverse('referral-history'), data)
        context = response.context
        self.assertEqual(len(context['referrals']), len(referrals))
        self.assertSetEqual(set([r.id for r in context['referrals']]),
                            set([r.id for r in referrals]))


class EditPhysicianViewTest(LoginBaseTest):
    def test_edit(self):
        organization = Organization.objects.create(org_name='org1')
        physician = Physician.objects.create(
            physician_name='phys1', organization=organization,
            physician_email='test@email.com', physician_phone='+442083660000',
            referral_special=False)
        data = {
            'organization': organization.id,
            'physician_name': 'new_name',
            'physician_phone': '+442083661177',
            'physician_email': 'new_email@email.com',
            'referral_special': 'on'
        }
        response = self.client.post(
            reverse('edit-physician', args=(physician.id,)), data)
        self.assertEqual(response.status_code, 200)
        physician = Physician.objects.get(id=physician.id)
        self.assertEqual(physician.physician_name, data['physician_name'])
        self.assertEqual(physician.physician_phone, data['physician_phone'])
        self.assertEqual(physician.physician_email, data['physician_email'])
        self.assertEqual(physician.referral_special, True)


class EditOrganizationViewTest(LoginBaseTest):
    def test_edit(self):
        organization = Organization.objects.create(
            org_name='phys1', org_contact_name="contact1",
            org_email='test@email.com', org_phone='+442083660000',
            org_special=False)
        data = {
            'org_name': 'new_name',
            'org_contact_name': 'new_contact',
            'org_phone': '+442083661177',
            'org_email': 'new_email@email.com',
            'org_special': 'on'
        }
        response = self.client.post(
            reverse('edit-organization', args=(organization.id,)), data)
        self.assertEqual(response.status_code, 200)
        organization = Organization.objects.get(id=organization.id)
        self.assertEqual(organization.org_name, data['org_name'])
        self.assertEqual(organization.org_contact_name,
                         data['org_contact_name'])
        self.assertEqual(organization.org_phone, data['org_phone'])
        self.assertEqual(organization.org_email, data['org_email'])
        self.assertEqual(organization.org_special, True)
