import os

from django.conf import settings


SCREENSHOT_DUMP_LOCATION = os.path.join(settings.BASE_DIR, 'screendumps')
