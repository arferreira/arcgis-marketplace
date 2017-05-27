from pathlib import Path

from django.test import TestCase
from arcgis_marketplace import factories


class FieldsTests(TestCase):

    def test_compress_field(self):
        obj = factories.WebMapingAppFactory(file__from_path='tests/test.zip')
        outpath = Path(obj.file.path).with_suffix('')

        self.assertTrue(Path(outpath).is_dir())
