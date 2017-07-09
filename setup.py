import os
import re

from setuptools import setup, find_packages


def get_long_description():
    for filename in ('README.rst',):
        with open(filename, 'r') as f:
            yield f.read()


def get_version(package):
    with open(os.path.join(package, '__init__.py')) as f:
        pattern = r'^__version__ = [\'"]([^\'"]*)[\'"]'
        return re.search(pattern, f.read(), re.MULTILINE).group(1)


setup(
    name='django-arcgis-marketplace',
    version=get_version('arcgis_marketplace'),
    license='MIT',
    description='Arcgis marketplace app.',
    long_description='\n\n'.join(get_long_description()),
    author='mongkok',
    author_email='dani.pyc@gmail.com',
    maintainer='mongkok',
    url='https://github.com/flavors/arcgis-marketplace/',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'Django>=1.11',
        'arcgis-sdk>=0.0.12',
        'celery>=4.0.2',
        'django-core-flavor>=0.0.16',
        'django-filter>=1.0.2',
        'django-oauth-toolkit>=0.12.0',
        'django-orders-flavor>=0.0.4',
        'django-polymorphic>=1.2',
        'django-taggit>=0.22.1',
        'djangorestframework>=3.5.0',
        'Pillow>=4.1.1',
        'psycopg2>=2.6.2',
        'social-auth-app-django>=1.2.0',
        'sorl-thumbnail>=12.3'
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
    ],
    zip_safe=False,
    tests_require=[
        'Django>=1.11',
        'arcgis-sdk>=0.0.12',
        'celery>=4.0.2',
        'coverage>=4.4',
        'django-core-flavor>=0.0.16',
        'django-filter>=1.0.2',
        'django-oauth-toolkit>=0.12.0',
        'django-orders-flavor>=0.0.4',
        'django-polymorphic>=1.2',
        'django-taggit>=0.22.1',
        'djangorestframework>=3.5.0',
        'factory-boy>=2.8.1',
        'Faker>=0.7.11',
        'Pillow>=4.1.1',
        'psycopg2>=2.6.2',
        'responses>=0.5.1',
        'social-auth-app-django>=1.2.0',
        'sorl-thumbnail>=12.3'
    ],
    package_data={
        'arcgis_marketplace': [
            'templates/arcgis_marketplace/*',
            'locale/*/LC_MESSAGES/django.po',
            'locale/*/LC_MESSAGES/django.mo'
        ]
    }
)
