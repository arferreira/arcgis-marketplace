from django.core import exceptions
from django.test import TestCase

from arcgis_marketplace import factories
from arcgis_marketplace import validators

from . import factories as test_factories


class ValidatorsTests(TestCase):

    def test_validate_file_extension(self):
        obj = factories.WebMapingAppFactory()
        validators.validate_file_extension(obj.file)

    def test_validate_file_extension_validation_error(self):
        obj = factories.WebMapingAppFactory(file__filename='test.txt')

        with self.assertRaises(exceptions.ValidationError):
            validators.validate_file_extension(obj.file)

    def test_validate_zip_compression(self):
        obj = test_factories.WebMapingAppZipFactory()

        validators.validate_zip_compression(obj.file)

    def test_validate_zip_compression_validation_error(self):
        obj = factories.WebMapingAppFactory()

        with self.assertRaises(exceptions.ValidationError):
            validators.validate_zip_compression(obj.file)
