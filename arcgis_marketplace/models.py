import arcgis_sdk

from dateutil.relativedelta import relativedelta
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.postgres import fields as pg_fields
from django.core.files.base import ContentFile
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from core_flavor import models as core_models
from core_flavor.urls import reverse_host
from core_flavor.utils import camel_to_dashed

from model_utils import Choices
from orders_flavor import models as orders_models
from sorl.thumbnail import ImageField

from taggit import models as taggit_models
from taggit.managers import TaggableManager

from . import fields
from . import managers
from . import settings as arcgis_settings
from .utils import path_to_url


class Account(core_models.SoftDeletableModel,
              core_models.TimeStampedUUIDModel):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_('user'))

    avatar = ImageField(
        _('avatar'),
        blank=True,
        upload_to=core_models.UUIDUploadTo(
            arcgis_settings.ARCGIS_UPLOAD_THUMBNAILS_TO
        ))

    expired = models.DateTimeField(null=True)
    data = pg_fields.JSONField()

    items = models.ManyToManyField(
        'orders_flavor.Item',
        through='ItemInAccount',
        verbose_name=_('items'))

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.user)

    def __dir__(self):
        return super().__dir__() + list(self.data.keys())

    def __getattribute__(self, attr):
        try:
            return super().__getattribute__(attr)
        except AttributeError:
            if not attr.startswith('_') and attr in self.data:
                return self.data[attr]
            raise

    def get_absolute_url(self):
        return reverse_host(
            'arcgis-marketplace-api:v1:account-detail',
            args=(self.id.hex,),
            **arcgis_settings.FLAVOR_REVERSE_EXTRA_KWARGS
        )

    @property
    def social_auth(self):
        return self.user.social_auth.get(provider='arcgis')

    def client(self):
        return arcgis_sdk.ArcgisAPI(self.access_token)

    @property
    def api(self):
        if not hasattr(self, '_api'):
            if self.is_expired:
                self.refresh_expired_token()
            self._api = self.client()
        return self._api

    def refresh_expired_token(self):
        assert hasattr(settings, 'SOCIAL_AUTH_ARCGIS_KEY'), (
            'Missing "SOCIAL_AUTH_ARCGIS_KEY" settings var'
        )

        result = self.client().refresh_token(
            client_id=settings.SOCIAL_AUTH_ARCGIS_KEY,
            refresh_token=self.refresh_token)

        self.data['access_token'] = result['access_token']
        self.set_expiration(result['expires_in'])
        self.save()

    @property
    def is_expired(self):
        return self.expired + relativedelta(seconds=5) < timezone.now()

    def set_expiration(self, expires_in):
        self.expired = timezone.now() + relativedelta(seconds=expires_in)

    def me(self):
        data = self.api.user_detail(self.username)

        self.save_thumbnail(data.get('thumbnail'))
        self.data.update(camel_to_dashed(data))
        self.save()
        return data

    def self(self):
        return self.api.self()

    @property
    def groups(self):
        return self.me()['groups']

    def get_group(self, value, field=None):
        if field is None:
            field = 'id'

        return next((
            group for group in self.groups
            if group[field] == value
        ), None)

    @property
    def templates_group_id(self):
        if not hasattr(self, '_templates_group_id'):
            self._templates_group_id = (
                self.self()['templatesGroupQuery'].split(':')[-1]
            )
        return self._templates_group_id

    def get_or_create_default_group(self):
        name = arcgis_settings.ARCGIS_DEFAULT_GROUP_NAME
        group = self.get_group(name, field='title')

        if group is None:
            return self.api.create_group(title=name, access='public')['group']
        return group

    def get_group_for_apps(self):
        # Arcgis default group?
        if self.templates_group_id.startswith('esri'):
            return self.get_or_create_default_group()
        # Get template group
        return self.get_group(self.templates_group_id)

    def set_group_for_apps(self, group_id):
        """
        Group contains the apps to use in the configurable apps gallery
        """
        self.api.update_group(group_id, sortField='title', sortOrder='asc')
        self.api.update_self(templatesGroupQuery='id:{}'.format(group_id))

    def share_items(self, item_id, group_id):
        """
        Share the Esri default configurable apps to this group
        """
        group_replaced = group_id != self.templates_group_id

        if group_replaced:
            self.set_group_for_apps(group_id)

        # Share order item
        self.api.share_item(item_id, groups=group_id)

        if group_replaced:
            # Share other items
            for item in self.api.group_items(group_id)['items']:
                try:
                    self.api.share_item(item['id'], groups=group_id)
                except arcgis_sdk.ArcgisAPIError:
                    # Item has a Relationship Type that does not allow this
                    pass

    def add_item(self, configuration=None, **kwargs):
        item = self.api.add_item(username=self.username, **kwargs)

        if configuration is not None:
            # Json is not suported!!
            self.api.update_item(
                username=self.username,
                item_id=item['id'],
                data=urlencode({
                    'text': configuration
                }),
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            )
        return item

    @property
    def featured_groups(self):
        return self.self()['featuredGroups']

    @property
    def subscription_type(self):
        return self.self()['subscriptionInfo']['type']

    def save_thumbnail(self, thumbnail):
        if thumbnail and (
                not self.avatar.name or
                thumbnail != self.thumbnail):

            content = ContentFile(
                self.api.user_thumbnail(
                    username=self.username,
                    filename=thumbnail
                )
            )

            self.avatar.save(thumbnail, content, save=True)


class ItemInAccount(models.Model):
    account = models.ForeignKey(
        'Account',
        on_delete=models.CASCADE,
        related_name='items_in_account',
        verbose_name=_('account'))

    item = models.ForeignKey(
        'orders_flavor.Item',
        on_delete=models.CASCADE,
        verbose_name=_('item'))

    order = models.ForeignKey(
        'orders_flavor.Order',
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_('order'))

    arcgis_item = pg_fields.JSONField(_('arcgis item'))
    arcgis_group = pg_fields.JSONField(_('arcgis group'))

    # file = fields.SymlinkField(_('file'), blank=True, source='item.file')
    objects = managers.ItemInAccountManager()

    def __str__(self):
        return "{self.item.name} <{self.account}>".format(self=self)


class GenericUUIDTaggedItem(taggit_models.CommonGenericTaggedItemBase,
                            taggit_models.TaggedItemBase):

    object_id = models.UUIDField(editable=False)


class AbstractItem(core_models.SoftDeletableModel, orders_models.Item):
    owner = models.ForeignKey(
        'Account',
        on_delete=models.CASCADE,
        verbose_name=_('owner'))

    youtube_url = models.CharField(
        blank=True,
        max_length=200,
        validators=[
            RegexValidator(
                regex=r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$',
                message=_('Invalid youtube url')
            )
        ])

    objects = managers.ItemManager()
    tags = TaggableManager(blank=True, through=GenericUUIDTaggedItem)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_host(
            'arcgis-marketplace-api:v1:product-detail',
            args=(self.id.hex,),
            **arcgis_settings.FLAVOR_REVERSE_EXTRA_KWARGS)


class AbstractPurposeItem(AbstractItem):
    PURPOSES = Choices(
        ('ready_to_use', _('Ready to use')),
        ('configurable', _('Configurable')),
        ('self_configurable', _('Self configurable')),
        ('code_sample', _('Code sample'))
    )

    purpose = models.CharField(_('purpose'), choices=PURPOSES, max_length=32)

    configuration = pg_fields.JSONField(
        _('configuration'),
        blank=True,
        null=True)

    class Meta:
        abstract = True


class WebMapingApp(AbstractPurposeItem):
    APIS = Choices(
        ('javascript', _('Javascript')),
        ('flex', _('Flex')),
        ('silverlight', _('Silverlight')),
        ('web_adf', _('Web ADF')),
        ('other', _('Other'))
    )

    api = models.CharField(_('api'), choices=APIS, max_length=32)

    file = fields.CompressField(
        upload_to=core_models.UUIDUploadTo(
            arcgis_settings.ARCGIS_UPLOAD_ITEM_TO
        ))

    preview = fields.SymlinkField(_('preview'), blank=True, source='file')

    url_query = pg_fields.JSONField(
        _('Url query string'),
        blank=True,
        null=True)

    @property
    def preview_url(self):
        return path_to_url(self.preview)
