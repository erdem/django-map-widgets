VERSION = (0, 3, 2)
__version__ = '.'.join(map(str, VERSION))

from .widgets import GoogleMapPointFieldWidget, GoogleMapPointFieldInlineWidget, \
    GoogleMapPointFieldStaticWidget, GoogleMapPointFieldStaticOverlayWidget, MapboxPointFieldWidget, LeafletPointFieldWidget

__all__ = [
    'GoogleMapPointFieldWidget', 'GoogleMapPointFieldInlineWidget',
    'GoogleMapPointFieldStaticWidget', 'GoogleMapPointFieldStaticOverlayWidget',
    'MapboxPointFieldWidget', 'LeafletPointFieldWidget'
]
