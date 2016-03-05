from django.test import TestCase
from datetime import datetime , timedelta, date

from tracking.models import Physician, Referral, Organization


class OrganizationTest(TestCase):
    ''' a testcases class for Organization model '''

    def setUp(self):
        ''' setup initial objects '''

        self.organization = Organization.objects.create(org_name='org1')

    def test_get_physician_no_physician(self):
        ''' quantifiedcode: ignore it! '''

        self.assertEqual(self.organization.get_physician().count(), 0)

    def test_get_physician(self):
        ''' quantifiedcode: ignore it! '''

        Physician.objects.create(
            physician_name='phys1', organization_id=self.organization.id)
        self.assertEqual(self.organization.get_physician().count(), 1)

    def test_get_physician_sorting(self):
        ''' quantifiedcode: ignore it! '''

        p1 = Physician.objects.create(
            physician_name='phys2', organization_id=self.organization.id)
        p2 = Physician.objects.create(
            physician_name='Phys1', organization_id=self.organization.id)
        p3 = Physician.objects.create(
            physician_name='phys4', organization_id=self.organization.id)
        p4 = Physician.objects.create(
            physician_name='Phys3', organization_id=self.organization.id)
        physicians = list(self.organization.get_physician().all())
        self.assertEqual(len(physicians), 4)
        self.assertEqual(physicians[0], p2)
        self.assertEqual(physicians[-1], p3)


class PhysicianTest(TestCase):
    ''' a testcases class for Physician model '''

    def setUp(self):
        ''' setup initial objects '''

        self.organization = Organization.objects.create(org_name='org1')
        self.physician = Physician.objects.create(
            physician_name='phys1', organization_id=self.organization.id)

    def test_get_referral_no_referral(self):
        ''' quantifiedcode: ignore it! '''

        params = {
            'to_date': datetime.now().date(),
            'from_date': (datetime.now() - timedelta(days=1)).date()
        }

        self.assertEqual(self.physician.get_referral(params).count(), 0)

    def test_get_referral_today(self):
        ''' quantifiedcode: ignore it! '''

        physician2 = Physician.objects.create(
            physician_name='phys2', organization_id=self.organization.id)
        referrals = [Referral.objects.create(physician=self.physician)
                     for _ in range(10)]
        not_related_referral = Referral.objects.create(physician=physician2)
        today = datetime.now().date()
        params = {
            'to_date': today,
            'from_date': today
        }
        p_referrals = self.physician.get_referral(params).all()

        self.assertEqual(len(p_referrals), 1)
        self.assertEqual(p_referrals[0]['visit'], 10)
        self.assertEqual(p_referrals[0]['visit_date'], today)

    def test_get_referral_10_days(self):
        ''' quantifiedcode: ignore it! '''

        today = datetime.now().date()
        referrals = [
            Referral.objects.create(physician=self.physician,
                                    visit_date=today + timedelta(days=i))
            for i in range(10)]
        referrals.reverse()
        params = {
            'to_date': today + timedelta(days=10),
            'from_date': today
        }
        p_referrals = self.physician.get_referral(params).all()

        self.assertEqual(len(p_referrals), 10)
        self.assertSetEqual({p['visit'] for p in p_referrals}, {1})
        self.assertListEqual([p['visit_date'] for p in p_referrals],
                             [r.visit_date for r in referrals])
