import responses

from rest_framework import status

from ...shortcuts import add_response
from ...views import BaseViewTests


class MeViewTests(BaseViewTests):

    @responses.activate
    def test_me_200_OK(self):
        response = self.client.get(self.reverse('me-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'test')

    @responses.activate
    def test_me_items_200_OK(self):
        add_response(
            'GET',
            'content/users/test',
            json={'total': 1}
        )

        response = self.client.get(self.reverse('me-items'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @responses.activate
    def test_me_groups_200_OK(self):
        add_response(
            'GET',
            'community/users/test',
            json={'groups': []}
        )

        response = self.client.get(self.reverse('me-groups'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
