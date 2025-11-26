"""
ASGI config for Central Rock Gym Route Tracking System.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'central_rock_tracker.settings')

application = get_asgi_application()
