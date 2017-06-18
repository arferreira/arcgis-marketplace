import factory
import factory.fuzzy

from django.utils.timezone import utc

from core_flavor import factories as core_factories
from orders_flavor import factories as orders_factories

from . import models


class UserFactory(core_factories.UserFactory):

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
        username='test')

    expired = factory.Faker(
        'date_time_between',
        start_date='+1d',
        end_date='+2d',
        tzinfo=utc)

    class Meta:
        model = 'arcgis_marketplace.Account'


class ExpiredAccountFactory(AccountFactory):
    expired = factory.Faker(
        'date_time_between',
        end_date='-1d',
        tzinfo=utc)


class AbstractItemFactory(orders_factories.ItemFactory):
    owner = factory.SubFactory(AccountFactory)

    class Meta:
        abstract = True


class PurposeItemFactory(AbstractItemFactory):
    purpose = factory.fuzzy.FuzzyChoice(
        choices=models.WebMapingApp.PURPOSES._db_values)

    class Meta:
        abstract = True


class WebMapingAppFactory(PurposeItemFactory):
    file = factory.django.FileField(filename='test.zip')
    api = factory.fuzzy.FuzzyChoice(
        choices=models.WebMapingApp.APIS._db_values)

    class Meta:
        model = 'arcgis_marketplace.WebMapingApp'
