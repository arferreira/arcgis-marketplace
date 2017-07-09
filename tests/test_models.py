import responses

from django.test import TestCase
from arcgis_marketplace import factories

from .api.shortcuts import add_response
from . import factories as test_factories


class ModelsTests(TestCase):

    def test_account_str(self):
        account = factories.AccountFactory()
        self.assertEqual(str(account), str(account.user))

    def test_account_dir(self):
        account = factories.AccountFactory()
        self.assertIn('access_token', dir(account))

    def test_account_getattribute(self):
        account = factories.AccountFactory()
        self.assertEqual(account.access_token, 'test')

    def test_account_social_auth(self):
        account = factories.AccountFactory()
        self.assertEqual(account.social_auth, account.user.social_auth.get())

    def test_account_client(self):
        account = factories.AccountFactory()
        self.assertEqual(account.client().access_token, account.access_token)

    def test_account_api(self):
        account = factories.AccountFactory()
        self.assertEqual(account.api.access_token, account.access_token)

    def test_account_api_default(self):
        account = factories.AccountFactory()
        account._api = True
        self.assertTrue(account.api)

    @responses.activate
    def test_account_refresh_expired_token(self):
        add_response(
            'GET',
            'oauth2/token/',
            json={
                'access_token': 'new!',
                'expires_in': 1800
            }
        )

        account = factories.ExpiredAccountFactory()
        account.api

        self.assertFalse(account.is_expired)
        self.assertEqual(account.access_token, 'new!')

    @responses.activate
    def test_me(self):
        add_response(
            'GET',
            'community/users/test',
            json={'test': True}
        )

        account = factories.AccountFactory()
        account.me()

        self.assertTrue(account.test)

    @responses.activate
    def test_featured_groups(self):
        add_response(
            'GET',
            'portals/self',
            json={'featuredGroups': []}
        )

        account = factories.AccountFactory()
        self.assertIsInstance(account.featured_groups, list)

    @responses.activate
    def test_subscription_type(self):
        add_response(
            'GET',
            'portals/self',
            json={'subscriptionInfo': {'type': 'test'}}
        )

        account = factories.AccountFactory()
        self.assertEqual(account.subscription_type, 'test')

    def test_item_str(self):
        item = test_factories.WebMapingAppZipFactory()
        self.assertEqual(str(item), item.name)
