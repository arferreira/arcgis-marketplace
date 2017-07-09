from core_flavor.api import fields as core_fields
from rest_framework import serializers

from ... import models
from .. import fields


__all__ = ['AccountSerializer', 'WebMapingAppSerializer']


class AccountBasicSerializer(serializers.ModelSerializer):

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


class AccountSerializer(AccountBasicSerializer):

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
    owner = AccountBasicSerializer(read_only=True)
    configuration = serializers.JSONField(required=False)
    url_query = serializers.JSONField(required=False)
    preview = fields.PreviewField(required=False)
    tags = core_fields.TaggitField()

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        instance = super().create(validated_data)
        instance.tags.set(*tags)
        return instance

    class Meta:
        model = models.WebMapingApp
        fields = (
            'owner', 'youtube_url', 'purpose', 'api', 'file', 'preview',
            'configuration', 'url_query', 'tags'
        )

        extra_kwargs = {
            'file': {'write_only': True}
        }
