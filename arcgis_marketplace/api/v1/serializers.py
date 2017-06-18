from rest_framework import serializers

from ... import models


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

    class Meta:
        model = models.WebMapingApp
        fields = (
            'owner', 'youtube_url', 'purpose', 'api', 'file', 'preview',
            'configuration'
        )

        extra_kwargs = {
            'file': {'write_only': True}
        }
