from pathlib import Path

from django.db import models
from django.contrib.sites.models import Site

from core_flavor import managers as core_managers
from orders_flavor import managers as orders_managers


__all__ = ['ItemManager']


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
        'self_configurable': 'selfConfigured',
        'code_sample': 'Code Sample'
    }

    def create_item(self, account, item, **kwargs):
        url = 'https://{domain}{path}'.format(
            domain=Site.objects.get_current().domain,
            path=Path(item.file.url).with_suffix('')
        )

        # TODO: Add thumbnail url and fix purpose field
        arcgis_item = account.add_item(
            title=item.name,
            type='Web Mapping Application',
            purpose=self.ARCGIS_PURPOSES[item.purpose],
            url=url,
            tags=item.comma_separated_tags)

        return self.create(
            account=account,
            item=item,
            arcgis_item=arcgis_item,
            **kwargs)
