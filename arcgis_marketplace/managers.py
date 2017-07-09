from django.db import models

from core_flavor import managers as core_managers
from orders_flavor import managers as orders_managers

from .utils import get_full_url


__all__ = ['ItemManager', 'ItemInAccountManager']


class BaseItemManager(orders_managers.BaseItemManager):
    pass


class ItemQuerySet(core_managers.SoftDeletableQuerySet,
                   orders_managers.ItemQuerySet):
    pass


ItemManager = BaseItemManager.from_queryset(ItemQuerySet)


class ItemInAccountManager(models.Manager):
    ARCGIS_PURPOSES = {
        'ready_to_use': 'Ready To Use',
        'configurable': 'Configurable',
        'self_configurable': 'selfConfigured,Configurable',
        'code_sample': 'Code Sample'
    }

    def create_item(self, account, item, **kwargs):
        data = {
            'title': item.name,
            'type': 'Web Mapping Application',
            'typeKeywords':
            'Map,Mapping Site,Online Map,Web Map,{api},{purpose}'.format(
                api=item.get_api_display(),
                purpose=self.ARCGIS_PURPOSES[item.purpose]
            ),
            'overwrite': 'false',
            'text': item.configuration,
            'url': get_full_url(item.preview_url),
            'tags': item.comma_separated_tags
        }

        if item.image:
            data['thumbnailurl'] = get_full_url(item.image.url)

        arcgis_item = account.add_item(
            configuration=item.configuration,
            **data)

        return self.create(
            account=account,
            item=item,
            arcgis_item=arcgis_item,
            **kwargs)
