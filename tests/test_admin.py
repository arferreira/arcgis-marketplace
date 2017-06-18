from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from arcgis_marketplace import admin
from arcgis_marketplace import factories
from arcgis_marketplace import models


class MockRequest:
    pass


request = MockRequest()


class AdminTests(TestCase):

    def setUp(self):
        self.site = AdminSite()

    def test_admin_account(self):
        account = factories.AccountFactory(
            data=dict(
                username='test',
                first_name='test',
                last_name='test',
                user_type='test',
                role='test',
                org_id='test'
            ))

        model_admin = admin.AccountAdmin(models.Account, self.site)

        self.assertIn('user', model_admin.get_fields(request))

        for field in model_admin.list_display:
            admin_field = getattr(model_admin, field, None)

            if admin_field is not None:
                self.assertIsInstance(admin_field(account), str)

    def test_admin_webmapingapp(self):
        model_admin = admin.WebMapingAppAdmin(models.WebMapingApp, self.site)
        self.assertIn('name', model_admin.get_fields(request))
