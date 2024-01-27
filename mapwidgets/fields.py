from django.db import models
from django.db.models.query_utils import DeferredAttribute
from django.utils.regex_helper import _lazy_re_compile

_re_point = _lazy_re_compile(
    r"\s*POINT\s*\((?P<lon>[-+]?(?:\d+(?:\.\d*)?|\.\d+))\s+(?P<lat>[-+]?(?:\d+(?:\.\d*)?|\.\d+))\)\s*"
)


class WKTPoint:
    """
    Mimics Django's built-in `django.contrib.gis.geos.point.Point` class
    """

    def __init__(self, x=None, y=None):
        if isinstance(x, (tuple, list)):
            self.x, self.y = x
        elif isinstance(x, str):
            match = _re_point.fullmatch(x)
            if not match:
                raise TypeError("WKTPoint: String input unrecognized as WKT POINT")
            self.x = float(match.group("lon"))
            self.y = float(match.group("lat"))
        else:
            self.x, self.y = x, y

    @property
    def tuple(self):
        return self.x, self.y

    @tuple.setter
    def tuple(self, tup):
        self.x, self.y = tup

    coords = tuple
    srid = None

    def __str__(self):
        return f"POINT({self.x:.7f} {self.y:.7f})"

    def __iter__(self):
        for f in ('x', 'y'):
            yield getattr(self, f)

    def __len__(self):
        return 2

    def __getitem__(self, index):
        return [self.x, self.y][index]

    def __copy__(self):
        return WKTPoint(self.x, self.y)


class WKTPointDescriptor(DeferredAttribute):
    def __get__(self, instance, cls=None):
        if instance is None:
            return self

        point = super().__get__(instance, cls)

        if point is None or not isinstance(point, WKTPoint):
            attr = WKTPoint(point)
            instance.__dict__[self.field.attname] = attr

        return instance.__dict__[self.field.attname]

    def __set__(self, instance, value):
        instance.__dict__[self.field.attname] = value


class WKTPointField(models.CharField):
    description = "POINT stored in WKT format with geos Point interface"
    descriptor_class = WKTPointDescriptor

    def __init__(self, *args, max_length=50, **kwargs):
        super().__init__(*args, max_length=max_length, **kwargs)
