import arcgis_sdk
import responses

from rest_framework import status


def add_response(method, path, **kwargs):
    kwargs.setdefault('status', status.HTTP_200_OK)
    kwargs.setdefault('content_type', 'application/json')

    responses.add(
        getattr(responses, method),
        arcgis_sdk.ARCGIS_API_URL + path,
        **kwargs
    )
