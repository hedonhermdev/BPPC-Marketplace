import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marketplace.settings")
django.setup()
