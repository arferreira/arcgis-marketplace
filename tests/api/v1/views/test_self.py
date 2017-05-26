import responses

from rest_framework import status

from ...shortcuts import add_response
from ...views import BaseViewTests


class SelfViewTests(BaseViewTests):

    @responses.activate
    def test_self_200_OK(self):
        add_response(
            'GET',
            'portals/self',
            json={'name': 'test-self'}
        )

        response = self.client.get(self.reverse('self-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test-self')

    @responses.activate
    def test_self_roles_200_OK(self):
        add_response(
            'GET',
            'portals/self/roles',
            json={'total': 1}
        )

        response = self.client.get(self.reverse('self-roles'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @responses.activate
    def test_self_users_200_OK(self):
        add_response(
            'GET',
            'portals/self/users',
            json={'total': 1}
        )

        response = self.client.get(self.reverse('self-users'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
