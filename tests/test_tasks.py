import responses

from django.test import TestCase

from arcgis_marketplace import factories
from arcgis_marketplace import tasks

from . import factories as test_factories
from .api.shortcuts import add_response


class TasksTests(TestCase):

    @responses.activate
    def test_tasks_add_item_to_account(self):
        arcgis_item_id = 'item-id'
        arcgis_group_id = 'group-id'

        add_response(
            'GET',
            'portals/self',
            json={'templatesGroupQuery': 'id:{}'.format(arcgis_group_id)}
        )

        add_response(
            'GET',
            'community/users/test',
            json={'groups': [{
                'id': arcgis_group_id
            }]}
        )

        add_response(
            'POST',
            'content/users/test/addItem',
            json={
                'id': arcgis_item_id,
                'success': True
            }
        )

        add_response(
            'POST',
            'content/items/{}/share'.format(arcgis_item_id),
            json={'itemId': arcgis_item_id}
        )

        account = factories.AccountFactory()
        item = test_factories.WebMapingAppZipFactory()

        tasks.add_item_to_account(account.id, item.id, group=None)

        item_in_account = account.items_in_account.get()

        self.assertEqual(account.items.get(), item)
        self.assertEqual(item_in_account.item, item)

        self.assertEqual(item_in_account.arcgis_item['id'], arcgis_item_id)
        self.assertEqual(item_in_account.arcgis_group['id'], arcgis_group_id)
