from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from tracking.models import Organization, Clinic, ClinicUser, \
    ReferringEntity, ReferringReportSetting, ClinicUserReportSetting


class LoginBaseTest(APITestCase):
    ''' a base class for rest testcases which need login '''

    def setUp(self):
        '''initial default user to be login in '''
        self.default_pass = 'pass1234'
        self.user = User.objects.create_superuser(username='user1',
                                                  email='user1@email.com',
                                                  password=self.default_pass)
        self.clinic = Clinic.objects.create(clinic_name="clinic1")
        self.clinic_user = ClinicUser.objects.create(
            clinic=self.clinic,
            user=self.user)

    def _login(self):
        ''' do login on client '''

        return self.client.login(username=self.user.username,
                                 password=self.default_pass)


class OrganizationTest(LoginBaseTest):
    ''' testcases class for Organization Rest api '''

    def test_add(self):
        ''' add api test '''

        self._login()
        url = reverse('rest_api:organization-list')
        data = {'org_name': 'org1', 'clinic': self.clinic.id}
        self.assertEqual(Organization.objects.count(), 0)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Organization.objects.count(), 1)
        self.assertEqual(Organization.objects.get().org_name, 'org1')

    def test_add_not_authorized(self):
        ''' call add api while not authorized '''

        url = reverse('rest_api:organization-list')
        data = {'org_name': 'org1', 'clinic': self.clinic.id}
        self.assertEqual(Organization.objects.count(), 0)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Organization.objects.count(), 0)

    def test_get(self):
        ''' get api test '''

        self._login()
        org1 = Organization.objects.create(org_name='org1', clinic=self.clinic)
        url = reverse('rest_api:organization-detail', args=(org1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['org_name'], 'org1')

    def test_get_not_authorized(self):
        ''' call get api while not authorized '''

        org1 = Organization.objects.create(org_name='org1', clinic=self.clinic)
        url = reverse('rest_api:organization-detail', args=(org1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update(self):
        ''' update api test '''

        self._login()
        org1 = Organization.objects.create(org_name='org1', clinic=self.clinic)
        url = reverse('rest_api:organization-detail', args=(org1.id,))
        data = {'org_name': 'org2'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Organization.objects.count(), 1)
        org1 = Organization.objects.get(id=org1.id)
        self.assertEqual(org1.org_name, 'org2')

    def test_update_not_authorized(self):
        ''' call update api while not authorized '''

        org1 = Organization.objects.create(org_name='org1', clinic=self.clinic)
        url = reverse('rest_api:organization-detail', args=(org1.id,))
        data = {'org_name': 'org2'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list(self):
        ''' list api test '''

        orgs = [Organization.objects.create(org_name='org{0}'.format(i),
                                            clinic=self.clinic)
                for i in range(5)]
        self._login()
        url = reverse('rest_api:organization-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), len(orgs))

    def test_list_not_authorized(self):
        ''' call list api while not authorized '''

        url = reverse('rest_api:organization-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ReferringReportSettingTest(LoginBaseTest):
    ''' testcases class for Organization Rest api '''

    def test_add(self):
        ''' add api test '''

        self._login()
        url = reverse('rest_api:referringreportsetting-list')
        organization = Organization.objects.create(
            org_name='org1',
            clinic_id=self.clinic.id)
        referring_entity = ReferringEntity.objects.create(
            entity_name='phys1', organization_id=organization.id)

        data = {'enabled': True,
                'period': ReferringReportSetting.PERIOD_DAILY,
                'report_name': 'thankyou',
                'referring_entity': referring_entity.id}
        self.assertEqual(ReferringReportSetting.objects.count(), 0)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ReferringReportSetting.objects.count(), 1)
        rs = ReferringReportSetting.objects.get()
        self.assertEqual(rs.enabled, True)
        self.assertEqual(rs.period, ReferringReportSetting.PERIOD_DAILY)
        self.assertEqual(rs.report_name, 'thankyou')
        self.assertEqual(rs.referring_entity, referring_entity)

    def test_add_invalid(self):
        ''' add api test '''

        self._login()
        url = reverse('rest_api:referringreportsetting-list')
        organization = Organization.objects.create(
            org_name='org1',
            clinic_id=self.clinic.id)
        referring_entity = ReferringEntity.objects.create(
            entity_name='phys1', organization_id=organization.id)

        data = {'enabled': True,
                'period': 'Invalid',
                'report_name': 'thankyou',
                'referring_entity': referring_entity.id}
        self.assertEqual(ReferringReportSetting.objects.count(), 0)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_bulk(self):
        ''' add api test '''

        self._login()
        url = reverse('rest_api:referringreportsetting-list')
        organization = Organization.objects.create(
            org_name='org1',
            clinic_id=self.clinic.id)
        ref1 = ReferringEntity.objects.create(
            entity_name='phys1', organization_id=organization.id)

        ref2 = ReferringEntity.objects.create(
            entity_name='phys2', organization_id=organization.id)

        data = {'enabled': True,
                'period': ReferringReportSetting.PERIOD_DAILY,
                'report_name': 'thankyou',
                'referring_entity': '*',
                'bulk': True}
        self.assertEqual(ReferringReportSetting.objects.count(), 0)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ReferringReportSetting.objects.count(), 2)
        rs = ReferringReportSetting.objects.all()
        self.assertSetEqual({r.referring_entity.id for r in rs},
                            {ref1.id, ref2.id})


class ClinicUserReportSettingTest(LoginBaseTest):
    ''' testcases class for Organization Rest api '''

    def test_add(self):
        ''' add api test '''

        self._login()
        url = reverse('rest_api:clinicuserreportsetting-list')

        data = {'enabled': True,
                'period': ClinicUserReportSetting.PERIOD_DAILY,
                'report_name': 'visit_history',
                'clinic_user': self.clinic_user.id}
        self.assertEqual(ClinicUserReportSetting.objects.count(), 0)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ClinicUserReportSetting.objects.count(), 1)
        rs = ClinicUserReportSetting.objects.get()
        self.assertEqual(rs.enabled, True)
        self.assertEqual(rs.period, ClinicUserReportSetting.PERIOD_DAILY)
        self.assertEqual(rs.report_name, 'visit_history')
        self.assertEqual(rs.clinic_user, self.clinic_user)

    def test_add_invalid(self):
        ''' add api test '''

        self._login()
        url = reverse('rest_api:clinicuserreportsetting-list')
        data = {'enabled': True,
                'period': 'Invalid',
                'report_name': 'visit_history',
                'clinic_user': self.clinic_user.id}
        self.assertEqual(ClinicUserReportSetting.objects.count(), 0)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_bulk(self):
        ''' add api test '''

        self._login()
        url = reverse('rest_api:clinicuserreportsetting-list')
        user2 = User.objects.create_user(username='user2',
                                         email='user1@email.com',
                                         password=self.default_pass)
        clinic_user2 = ClinicUser.objects.create(
            clinic=self.clinic,
            user=user2)

        data = {'enabled': True,
                'period': ClinicUserReportSetting.PERIOD_DAILY,
                'report_name': 'visit_history',
                'clinic_user': '*',
                'bulk': True}
        self.assertEqual(ClinicUserReportSetting.objects.count(), 0)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ClinicUserReportSetting.objects.count(), 2)
        rs = ClinicUserReportSetting.objects.all()
        self.assertSetEqual({r.clinic_user.id for r in rs},
                            {self.clinic_user.id, clinic_user2.id})
