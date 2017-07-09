from pathlib import Path

from django.conf import settings
from django.contrib.sites.models import Site


def path_to_url(path):
    return ('/' / Path(path).relative_to(settings.SITE_DIR)).as_posix()


def get_full_url(path):
    return ''.join(['https://', Site.objects.get_current().domain, path])
