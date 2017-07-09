#!/usr/bin/env python

import os
import sys

from pathlib import Path

import django

from django.conf import settings
from django.test.runner import DiscoverRunner


DEFAULT_SETTINGS = dict(
    USE_TZ=True,
    SITE_ID=1,
    SITE_NAME='test',
    SITE_DIR=Path(__file__).resolve().parent,
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'django_filters',
        'oauth2_provider',
        'paypal.standard.ipn',
        'polymorphic',
        'rest_framework',
        'social_django',
        'taggit',
        'core_flavor.apps.CoreAppConfig',
        'countries_flavor.apps.CountriesAppConfig',
        'orders_flavor.apps.OrdersAppConfig',
        'arcgis_marketplace.apps.ArcgisMarketplaceAppConfig',
        'tests'
    ),
    DATABASES={
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': os.environ['POSTGRES_DB_NAME'],
            'USER': os.environ.get('POSTGRES_DB_USER', 'postgres'),
            'PASSWORD': os.environ.get('POSTGRES_DB_PASSWORD', '')
        }
    },
    ROOT_URLCONF='tests.urls',
    BROKER_URL='memory://',
    REST_FRAMEWORK={
        'DEFAULT_FILTER_BACKENDS': (
            'rest_framework_filters.backends.DjangoFilterBackend',
            'rest_framework.filters.OrderingFilter',
            'rest_framework.filters.SearchFilter'
        ),
        'DEFAULT_PAGINATION_CLASS':
        'core_flavor.api.pagination.CursorPageNumberPagination',
        'PAGE_SIZE': 10,
        'TEST_REQUEST_DEFAULT_FORMAT': 'json'
    },
    MIDDLEWARE=[
        'core_flavor.api.middleware.VersioningMiddleware'
    ],
    SOCIAL_AUTH_ARCGIS_KEY='test',
    PAYPAL_BUSINESS='test',
    PAYPAL_TEST=True,
    ORDERS_ITEMS_SERIALIZERS=[
        'arcgis_marketplace.api.v1.serializers.WebMapingAppSerializer',
    ],
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'loaders': [
                'django.template.loaders.app_directories.Loader'
            ]
        }
    }]
)


def runtests():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)

    django.setup()

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    failures = DiscoverRunner(
        verbosity=1,
        interactive=True,
        failfast=False)\
        .run_tests(['tests'])

    sys.exit(failures)


if __name__ == '__main__':
    runtests()
