from celery import current_app

from . import models


@current_app.task()
def add_item_to_account(account, item, order=None, group=None):
    if group is None:
        group = account.get_group_for_apps()

    item_in_account = models.ItemInAccount.objects.create_item(
        account=account,
        item=item,
        order=order,
        arcgis_group=group)

    account.share_items(
        item_in_account.arcgis_item['id'],
        group['id'])
