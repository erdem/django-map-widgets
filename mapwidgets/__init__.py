VERSION = (0, 5, 0)
__version__ = ".".join(map(str, VERSION))

from .widgets import (
    GoogleMapPointFieldInlineWidget,
    GoogleMapPointFieldStaticWidget,
    GoogleMapPointFieldWidget,
    LeafletPointFieldWidget,
    MapboxPointFieldWidget,
)

__all__ = [
    "GoogleMapPointFieldWidget",
    "GoogleMapPointFieldInlineWidget",
    "GoogleMapPointFieldStaticWidget",
    "MapboxPointFieldWidget",
    "LeafletPointFieldWidget",
]
