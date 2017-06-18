from arcgis_marketplace import factories


class WebMapingAppZipFactory(factories.WebMapingAppFactory):
    file__from_path = 'tests/test.zip'
