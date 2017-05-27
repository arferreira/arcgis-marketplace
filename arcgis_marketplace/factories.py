import factory
import factory.fuzzy

from django.conf import settings
from django.utils.timezone import utc

from . import models


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker('email')

    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('email',)

    @factory.post_generation
    def social_auth(self, create, extracted, **kwargs):
        if create:
            UserSocialAuthFactory(user=self, provider='arcgis')


class UserSocialAuthFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    uid = factory.fuzzy.FuzzyText(length=16)

    class Meta:
        model = 'social_django.UserSocialAuth'


class AccountFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    data = dict(
        access_token='test',
        refresh_token='test',
        username='test'
    )

    expired = factory.Faker(
        'date_time_between',
        start_date='+1d',
        end_date='+2d',
        tzinfo=utc
    )

    class Meta:
        model = 'arcgis_marketplace.Account'


class ExpiredAccountFactory(AccountFactory):
    expired = factory.Faker(
        'date_time_between',
        end_date='-1d',
        tzinfo=utc
    )


class ItemFactory(factory.django.DjangoModelFactory):
    owner = factory.SubFactory(AccountFactory)
    title = factory.fuzzy.FuzzyText(length=255)
    price = factory.fuzzy.FuzzyFloat(1, 100)

    class Meta:
        model = 'arcgis_marketplace.Item'


class PurposeItemFactory(ItemFactory):
    purpose = factory.fuzzy.FuzzyChoice(
        choices=models.WebMapingApp.PURPOSES._db_values
    )

    class Meta:
        abstract = True


class WebMapingAppFactory(PurposeItemFactory):
    file = factory.django.FileField(filename='test.zip')

    class Meta:
        model = 'arcgis_marketplace.WebMapingApp'
