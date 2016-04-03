from django.test import TestCase
from datetime import datetime , timedelta, date

from tracking.models import Clinic, ReferringEntity, TreatingProvider, PatientVisit, Organization


class OrganizationTest(TestCase):
    ''' a testcases class for Organization model '''

    def setUp(self):
        ''' setup initial objects '''

        self.clinic = Clinic.objects.create(clinic_name="clinic1")
        self.organization = Organization.objects.create(
            org_name='org1', clinic=self.clinic)

    def test_get_referring_entity_no_referring_entity(self):
        ''' quantifiedcode: ignore it! '''

        self.assertEqual(self.organization.get_referring_entity().count(), 0)

    def test_get_referring_entity(self):
        ''' quantifiedcode: ignore it! '''

        ReferringEntity.objects.create(
            entity_name='phys1', organization_id=self.organization.id)
        self.assertEqual(self.organization.get_referring_entity().count(), 1)

    def test_get_referring_entity_sorting(self):
        ''' quantifiedcode: ignore it! '''

        p1 = ReferringEntity.objects.create(
            entity_name='phys2', organization_id=self.organization.id)
        p2 = ReferringEntity.objects.create(
            entity_name='Phys1', organization_id=self.organization.id)
        p3 = ReferringEntity.objects.create(
            entity_name='phys4', organization_id=self.organization.id)
        p4 = ReferringEntity.objects.create(
            entity_name='Phys3', organization_id=self.organization.id)
        referring_entitys = list(self.organization.get_referring_entity().all())
        self.assertEqual(len(referring_entitys), 4)
        self.assertEqual(referring_entitys[0], p2)
        self.assertEqual(referring_entitys[-1], p3)


class ReferringEntityTest(TestCase):
    ''' a testcases class for ReferringEntity model '''

    def setUp(self):
        ''' setup initial objects '''

        self.clinic = Clinic.objects.create(clinic_name='clinic1')
        self.organization = Organization.objects.create(
            org_name='org1',
            clinic_id=self.clinic.id)
        self.referring_entity = ReferringEntity.objects.create(
            entity_name='phys1', organization_id=self.organization.id)
        self.treating_provider = TreatingProvider.objects.create(
            clinic=self.clinic, provider_name="ent1", provider_type="D") 

    def test_get_patient_visit_no_patient_visit(self):
        ''' quantifiedcode: ignore it! '''

        params = {
            'to_date': datetime.now().date(),
            'from_date': (datetime.now() - timedelta(days=1)).date()
        }

        self.assertEqual(
            self.referring_entity.get_patient_visit(params, self.clinic).count(),
            0)

    def test_get_patient_visit_today(self):
        ''' quantifiedcode: ignore it! '''

        referring_entity2 = ReferringEntity.objects.create(
            entity_name='phys2', organization_id=self.organization.id)
        patient_visits = [PatientVisit.objects.create(
                    referring_entity=self.referring_entity,
                    treating_provider=self.treating_provider)
                     for _ in range(10)]
        not_related_patient_visit = PatientVisit.objects.create(referring_entity=referring_entity2)
        today = datetime.now().date()
        params = {
            'to_date': today,
            'from_date': today
        }
        p_patient_visits = self.referring_entity.get_patient_visit(params, self.clinic).all()

        self.assertEqual(len(p_patient_visits), 1)
        self.assertEqual(p_patient_visits[0]['visit'], 10)
        self.assertEqual(p_patient_visits[0]['visit_date'], today)

    def test_get_patient_visit_10_days(self):
        ''' quantifiedcode: ignore it! '''

        today = datetime.now().date()
        patient_visits = [
            PatientVisit.objects.create(
                referring_entity=self.referring_entity,
                treating_provider=self.treating_provider,
                visit_date=today + timedelta(days=i))
            for i in range(10)]
        patient_visits.reverse()
        params = {
            'to_date': today + timedelta(days=10),
            'from_date': today
        }
        p_patient_visits = self.referring_entity.get_patient_visit(params, self.clinic).all()

        self.assertEqual(len(p_patient_visits), 10)
        self.assertSetEqual({p['visit'] for p in p_patient_visits}, {1})
        self.assertListEqual([p['visit_date'] for p in p_patient_visits],
                             [r.visit_date for r in patient_visits])
