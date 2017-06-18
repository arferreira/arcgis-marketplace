from core_flavor import managers as core_managers
from orders_flavor import managers as orders_managers

__all__ = ['ItemManager']


class BaseItemManager(orders_managers.BaseItemManager):
    pass


class ItemQuerySet(core_managers.SoftDeletableQuerySet,
                   orders_managers.ItemQuerySet):
    pass


ItemManager = BaseItemManager.from_queryset(ItemQuerySet)
