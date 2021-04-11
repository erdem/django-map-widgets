VERSION = (0, 3, 1)
__version__ = '.'.join(map(str, VERSION))

from .widgets import GooglePointFieldWidget, GooglePointFieldInlineWidget, \
    GoogleStaticMapWidget, GoogleStaticOverlayMapWidget
