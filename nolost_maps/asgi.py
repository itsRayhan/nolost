"""ASGI config for nolost_maps project."""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nolost_maps.settings")
application = get_asgi_application()
