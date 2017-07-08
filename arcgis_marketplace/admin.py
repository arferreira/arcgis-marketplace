from django.contrib import admin
from polymorphic import admin as polymorphic_admin

from . import models


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'username', 'first_name', 'last_name', 'type', 'role',
        'organization_id', 'created', 'modified', 'expired', 'removed')

    list_filter = ('created', 'modified', 'expired', 'removed')

    def username(self, obj):
        return obj.username

    def first_name(self, obj):
        return obj.first_name

    def last_name(self, obj):
        return obj.last_name

    def type(self, obj):
        return obj.user_type

    def role(self, obj):
        return obj.role

    def organization_id(self, obj):
        return obj.org_id


@admin.register(models.ItemInAccount)
class ItemInAccountAdmin(admin.ModelAdmin):
    list_display = ('account', 'item', 'order')


class ItemChildAdmin(polymorphic_admin.PolymorphicChildModelAdmin):
    list_display = ['owner', 'name', 'price', 'created', 'removed']
    list_filter = ['owner', 'created', 'removed']


@admin.register(models.WebMapingApp)
class WebMapingAppAdmin(ItemChildAdmin):
    base_model = models.WebMapingApp
    list_display = ItemChildAdmin.list_display + ['purpose', 'file', 'api']
    list_filter = ItemChildAdmin.list_filter + ['purpose', 'api']
    exclude = ('preview',)
