VERSION = (0, 5, 0)
__version__ = ".".join(map(str, VERSION))

from .widgets import (
    GoogleMapPointFieldWidget,
    GoogleMapPointFieldInlineWidget,
    MapboxPointFieldWidget,
    LeafletPointFieldWidget,
)

__all__ = [
    "GoogleMapPointFieldWidget",
    "GoogleMapPointFieldInlineWidget",
    "MapboxPointFieldWidget",
    "LeafletPointFieldWidget",
]
