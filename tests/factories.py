from arcgis_marketplace import factories


class WebMapingAppTxtFactory(factories.WebMapingAppFactory):
    file__from_path = 'tests/test.txt'


class WebMapingAppZipFactory(factories.WebMapingAppFactory):
    file__from_path = 'tests/test.zip'
