VERSION = (0, 1, 8)
__version__ = '.'.join(map(str, VERSION))

from widgets import GooglePointFieldWidget, GooglePointFieldInlineWidget, \
    GoogleStaticMapWidget, GoogleStaticOverlayMapWidget
