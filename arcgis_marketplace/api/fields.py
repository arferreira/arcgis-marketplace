from rest_framework import serializers
from ..utils import path_to_url


class PreviewField(serializers.Field):

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        request = self.context.get('request', None)

        if request is not None:
            return request.build_absolute_uri(path_to_url(value))
        return value
