VERSION = (0, 6, 0)
__version__ = ".".join(map(str, VERSION))

from .widgets import (
    GoogleMapPointFieldInlineWidget,
    GoogleMapPointFieldStaticWidget,
    GoogleMapPointFieldWidget,
    LeafletPointFieldWidget,
    LeafletPolygonFieldWidget,
    MapboxPointFieldStaticWidget,
    MapboxPointFieldWidget,
)

__all__ = [
    "GoogleMapPointFieldWidget",
    "GoogleMapPointFieldInlineWidget",
    "GoogleMapPointFieldStaticWidget",
    "MapboxPointFieldWidget",
    "MapboxPointFieldStaticWidget",
    "LeafletPointFieldWidget",
    "LeafletPolygonFieldWidget",
]
