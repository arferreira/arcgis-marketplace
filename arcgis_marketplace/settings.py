from django.conf import settings


ARCGIS_DEFAULT_GROUP_NAME = getattr(
    settings,
    'ARCGIS_DEFAULT_GROUP_NAME',
    'Marketplace')

ARCGIS_UPLOAD_ITEM_TO = getattr(
    settings,
    'ARCGIS_UPLOAD_ITEM_TO',
    'arcgis/items/%Y/%m/')

ARCGIS_UPLOAD_THUMBNAILS_TO = getattr(
    settings,
    'ARCGIS_UPLOAD_THUMBNAILS_TO',
    'arcgis/thumbnails/%Y/%m/')

FLAVOR_REVERSE_EXTRA_KWARGS = getattr(
    settings,
    'FLAVOR_REVERSE_EXTRA_KWARGS',
    {})
