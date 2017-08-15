from django.urls import reverse
from core_flavor.api.test import APITestCase

from arcgis_marketplace import factories


class BaseViewTests(APITestCase):

    def setUp(self):
        self.account = factories.AccountFactory()
        self.user = self.account.user
        self.client.force_authenticate(user=self.account.user)

    @classmethod
    def reverse(cls, view_name, **kwargs):
        return reverse('arcgis-marketplace:api:{version}:{view_name}'.format(
            version=cls.VERSION,
            view_name=view_name
        ), **kwargs)
