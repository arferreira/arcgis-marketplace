from django.contrib import admin
from polymorphic import admin as polymorphic_admin
from sorl.thumbnail.admin import AdminImageMixin

from . import models


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'username', 'first_name', 'last_name', 'type', 'role',
        'organization_id', 'created', 'modified', 'expired', 'removed'
    )

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


@admin.register(models.Item)
class ItemAdmin(AdminImageMixin,
                polymorphic_admin.PolymorphicParentModelAdmin):

    base_model = models.Item
    child_models = (models.WebMapingApp,)

    list_display = ['owner', 'title', 'price', 'created', 'removed']
    list_filter = ['owner', 'created', 'removed']


class ItemChildAdmin(polymorphic_admin.PolymorphicChildModelAdmin):
    base_model = models.Item
    list_display = ItemAdmin.list_display
    list_filter = ItemAdmin.list_filter


@admin.register(models.WebMapingApp)
class WebMapingAppAdmin(ItemChildAdmin):
    base_model = models.WebMapingApp
    list_display = ItemAdmin.list_display + ['purpose', 'file', 'api']
    list_filter = ItemAdmin.list_filter + ['purpose', 'api']
