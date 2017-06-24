Django Arcgis Marketplace
=========================

|Waffle| |Pypi| |Wheel| |Build Status| |Codecov| |Code Climate|


Arcgis marketplace application.

Dependencies
------------

* Python ≥ 3.4
* Django ≥ 1.11
* Postgres


Installation
------------

Install last stable version from Pypi.

.. code:: sh

    pip install django-arcgis-marketplace


Add ``arcgis_marketplace`` to your INSTALLED_APPS setting.

.. code:: python

    INSTALLED_APPS = (
        ...
        'django_filters',
        'oauth2_provider',
        'paypal.standard.ipn',
        'polymorphic',
        'rest_framework',
        'social_django',
        'taggit',
        ...
        'core_flavor.apps.CoreAppConfig',
        'countries_flavor.apps.CountriesAppConfig',
        'orders_flavor.apps.OrdersAppConfig',
        'arcgis_marketplace.apps.ArcgisMarketplaceAppConfig'
    )

Hook the Django urls into your URLconf.

.. code:: python

    from django.conf.urls import include, url

    urlpatterns = [
        url(r'^', include(
            'arcgis_marketplace.urls',
            namespace='arcgis-marketplace')),

        url(r'^', include(
            'arcgis_marketplace.api.urls',
            namespace='arcgis-marketplace-api'))
    ]

Apply migrations.

.. code:: python

    python manage.py migrate


.. |Waffle| image:: https://badge.waffle.io/flavors/arcgis-marketplace.png?label=ready&title=Ready 
   :target: https://waffle.io/flavors/arcgis-marketplace?utm_source=badge
   :alt: 'Stories in Ready'

.. |Pypi| image:: https://img.shields.io/pypi/v/django-arcgis-marketplace.svg
   :target: https://pypi.python.org/pypi/django-arcgis-marketplace

.. |Wheel| image:: https://img.shields.io/pypi/wheel/django-arcgis-marketplace.svg
   :target: https://pypi.python.org/pypi/django-arcgis-marketplace

.. |Build Status| image:: https://travis-ci.org/flavors/arcgis-marketplace.svg?branch=master
   :target: https://travis-ci.org/flavors/arcgis-marketplace

.. |Codecov| image:: https://img.shields.io/codecov/c/github/flavors/arcgis-marketplace.svg
   :target: https://codecov.io/gh/flavors/arcgis-marketplace

.. |Code Climate| image:: https://codeclimate.com/github/flavors/arcgis-marketplace/badges/gpa.svg
   :target: https://codeclimate.com/github/flavors/arcgis-marketplace
