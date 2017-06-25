import responses

from rest_framework import status

from ...shortcuts import add_response
from ...views import BaseViewTests


class GroupiewTests(BaseViewTests):

    @responses.activate
    def test_group_list_200_OK(self):
        add_response(
            'GET',
            'community/groups',
            json={'total': 1}
        )

        response = self.client.get(
            self.reverse('group-list'), {
                'q': 'group'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @responses.activate
    def test_group_create_201_CREATED(self):
        add_response(
            'POST',
            'community/createGroup',
            json={'success': True}
        )

        response = self.client.post(
            self.reverse('group-list'), {
                'title': 'my item',
                'access': 'public'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @responses.activate
    def test_group_detail_200_OK(self):
        add_response(
            'GET',
            'community/groups/test',
            json={'id': 'test'}
        )

        response = self.client.get(
            self.reverse('group-detail', args=('test',))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 'test')

    @responses.activate
    def test_group_update_200_OK(self, method=None):
        add_response(
            'POST',
            'community/groups/test/update',
            json={'title': 'updated'}
        )

        if method is None:
            method = 'put'

        response = getattr(self.client, method)(
            self.reverse('group-detail', args=('test',)), {
                'title': 'updated'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'updated')

    def test_group_partial_update_200_OK(self):
        self.test_group_update_200_OK('patch')

    @responses.activate
    def test_group_delete_204_NO_CONTENT(self):
        add_response(
            'POST',
            'community/groups/test/delete',
            json={'success': True}
        )

        response = self.client.delete(
            self.reverse('group-detail', args=('test',))
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @responses.activate
    def test_group_add_200_OK(self, method=None):
        users = 'alice,bob'

        add_response(
            'POST',
            'community/groups/test/addUsers',
            json={'added': users.split(',')}
        )

        response = self.client.post(
            self.reverse('group-add', args=('test',)), {
                'users': users
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @responses.activate
    def test_group_invite_200_OK(self, method=None):
        users = 'alice,bob'

        add_response(
            'POST',
            'community/groups/test/invite',
            json={'success': True}
        )

        response = self.client.post(
            self.reverse('group-invite', args=('test',)), {
                'users': users
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @responses.activate
    def test_group_items_200_OK(self, method=None):
        add_response(
            'GET',
            'content/groups/test',
            json={'total': 1}
        )

        response = self.client.get(
            self.reverse('group-items', args=('test',))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @responses.activate
    def test_group_configurable_apps_200_OK(self, method=None):
        add_response(
            'POST',
            'portals/self',
            json={'success': True}
        )

        add_response(
            'POST',
            'community/groups/test/update',
            json={'title': 'updated'}
        )

        response = self.client.post(
            self.reverse('group-configurable-apps', args=('test',))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
