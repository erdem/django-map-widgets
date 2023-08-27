VERSION = (0, 3, 2)
__version__ = '.'.join(map(str, VERSION))

from .widgets import GooglePointFieldWidget, GooglePointFieldInlineWidget, \
    GoogleStaticMapWidget, GoogleStaticOverlayMapWidget, MapboxPointFieldWidget, OSMPointFieldWidget

__all__ = [
    'GooglePointFieldWidget', 'GooglePointFieldInlineWidget',
    'GoogleStaticMapWidget', 'GoogleStaticOverlayMapWidget',
    'MapboxPointFieldWidget', 'OSMPointFieldWidget'
]
