import responses

from django.test import TestCase

from social_core.backends.arcgis import ArcGISOAuth2
from social_core.backends.oauth import OAuthAuth

from arcgis_marketplace import factories
from arcgis_marketplace import pipeline

from .api.shortcuts import add_response


class PipelineTests(TestCase):

    def test_update_or_create_account(self):
        backend = ArcGISOAuth2()
        user = factories.UserFactory()

        pipeline.update_or_create_account(backend, user, dict(test=True))
        self.assertTrue(user.account.test)

    def test_update_or_create_account_unknown_backend(self):
        backend = OAuthAuth()
        user = factories.UserFactory()

        pipeline.update_or_create_account(backend, user, dict())
        self.assertFalse(hasattr(user, 'account'))

    def test_update_token_expiration(self):
        account = factories.ExpiredAccountFactory()
        social_auth = account.social_auth
        social_auth.extra_data = dict(expires_in=1800)

        pipeline.update_token_expiration(account, social_auth)
        self.assertFalse(account.is_expired)

    def test_update_token_expiration_missing_account(self):
        pipeline.update_token_expiration(account=None)

    @responses.activate
    def test_save_thumbnail(self):
        add_response(
            'GET',
            'community/users/test/info/me.png',
            content_type='image/png',
            body=':)',
            stream=True
        )

        account = factories.AccountFactory()
        pipeline.save_thumbnail({'thumbnail': 'me.png'}, account=account)

        self.assertEqual(account.avatar.file.read(), b':)')

    def test_save_thumbnail_missing_account(self):
        pipeline.save_thumbnail({}, account=None)
