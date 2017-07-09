from celery import current_app

from orders_flavor import models as orders_models
from . import models


@current_app.task()
def add_item_to_account(account_id, item_id, group=None):
    account = models.Account.objects.get(id=account_id)
    item = orders_models.Item.objects.get(id=item_id)

    if group is None:
        group = account.get_group_for_apps()

    item_in_account = models.ItemInAccount.objects.create_item(
        account=account,
        item=item,
        arcgis_group=group)

    account.share_items(
        item_in_account.arcgis_item['id'],
        group['id'])
