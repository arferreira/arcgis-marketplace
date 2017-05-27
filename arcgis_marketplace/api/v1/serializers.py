from core_flavor.api import fields as core_fields
from core_flavor.api import serializers as core_serializers

from rest_framework import serializers

from ... import models


__all__ = ['AccountSerializer', 'ItemSerializer']


class ItemAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Account
        fields = (
            'id', 'username', 'first_name', 'last_name', 'avatar',
            'region', 'created'
        )

        extra_kwargs = {
            'id': {'source': 'id.hex'}
        }

    def build_field(self, field_name, info, model_class, nested_depth):
        if not hasattr(model_class, field_name):
            return self.build_property_field(field_name, model_class)
        return super().build_field(field_name, info, model_class, nested_depth)


class AccountSerializer(ItemAccountSerializer):

    class Meta:
        model = models.Account
        fields = ('id', 'avatar', 'created')
        extra_kwargs = {
            'id': {'source': 'id.hex'}
        }

    def to_representation(self, instance):
        data = instance.data
        data.update(super().to_representation(instance))
        data.update(instance.data)
        return data


class WebMapingAppSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.WebMapingApp
        fields = ('purpose', 'api', 'file', 'preview', 'configuration')
        extra_kwargs = {
            'file': {'write_only': True}
        }


class ItemSerializer(core_serializers.PolymorphicSerializer):
    id = serializers.UUIDField(source='id.hex', read_only=True)
    owner = ItemAccountSerializer(read_only=True)
    price = core_fields.DecimalField()

    class Meta:
        model = models.Item
        fields = (
            'id', 'owner', 'title', 'description', 'price', 'image',
            'youtube_url', 'modified', 'created'
        )

        child_serializers = (
            WebMapingAppSerializer,
        )
