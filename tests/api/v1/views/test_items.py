import responses

from rest_framework import status

from ...shortcuts import add_response
from ...views import BaseViewTests


class ItemViewTests(BaseViewTests):

    @responses.activate
    def test_item_create_201_CREATED(self):
        add_response(
            'POST',
            'content/users/test/addItem',
            json={'success': True}
        )

        response = self.client.post(
            self.reverse('item-list'), {
                'title': 'my item',
                'type': 'Web Mapping Application'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])

    @responses.activate
    def test_item_detail_200_OK(self):
        add_response(
            'GET',
            'content/items/itemId',
            json={'id': 'test'}
        )

        response = self.client.get(
            self.reverse('item-detail', args=('itemId',))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 'test')

    @responses.activate
    def test_item_share_200_OK(self):
        add_response(
            'POST',
            'content/items/itemId/share',
            json={'itemId': 'test'}
        )

        response = self.client.post(
            self.reverse('item-share', args=('itemId',)), {
                'groups': 'group1,group2'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
