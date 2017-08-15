from django.conf.urls import include, url


urlpatterns = [
    url(r'^', include(
        'arcgis_marketplace.urls',
        namespace='arcgis-marketplace'))
]
