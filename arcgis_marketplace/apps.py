from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ArcgisMarketplaceAppConfig(AppConfig):
    name = 'arcgis_marketplace'
    verbose_name = _('Arcgis marketplace')

    def ready(self):
        import arcgis_marketplace.signals.loggers  # NOQA
