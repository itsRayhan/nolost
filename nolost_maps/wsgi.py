"""WSGI config for nolost_maps project."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nolost_maps.settings")
application = get_wsgi_application()
