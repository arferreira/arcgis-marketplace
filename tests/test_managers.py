import responses

from django.test import TestCase

from arcgis_marketplace import factories
from arcgis_marketplace import models

from . import factories as test_factories
from .api.shortcuts import add_response


class ManagersTests(TestCase):

    @responses.activate
    def test_create_item(self):
        add_response(
            'POST',
            'content/users/test/addItem',
            json={'success': True}
        )

        account = factories.AccountFactory()
        item = test_factories.WebMapingAppZipFactory()

        item_in_account = models.ItemInAccount.objects.create_item(
            account,
            item,
            arcgis_group={'test': True})

        self.assertEqual(item_in_account.account, account)
        self.assertEqual(item_in_account.item, item)

        self.assertTrue(item_in_account.arcgis_group['test'])
