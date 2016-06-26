from mapwidgets.settings import mw_settings

DEFAULT_GOOGLE_STATIC_MAP_CONFIGS = {
    "zoom": 15,
    "center": None,
    "size": "640x640",
    "scale": "1",
    "format": "png",
    "maptype": "roadmap",
    "markers": [],
    "path": [],
    "visible": None,
    "style": [],
    "language": None,
    "region": None,
    "key": mw_settings.GOOGLE_MAP_API_KEY,
    "signature": mw_settings.GOOGLE_MAP_API_SIGNATURE,
}


class GoogleStaticMapGenerater(object):
    MAPTYPES = ['roadmap', 'satellite', 'hybrid', 'terrain']
    FORMATS = ['png', 'png8', 'png32', 'gif', 'jpg', 'jpg-baseline']
    ZOOM_RANGE = list(range(1, 21))
    SCALE_RANGE = list(range(1, 5))

    def __init__(self, points, *args, **kwargs):
        self.points = points
        self.check_parameters()

    def check_parameters(self):
        if self.points is not list:
            raise TypeError('"points" parameter must be a list.')

        settings = self.settings

        if settings.zoom is not None and settings.zoom not in GoogleStaticMapGenerater.ZOOM_RANGE:
            raise ValueError(
                "[%s] is not a zoom setting. Must be between %s and %s" %
                (settings.zoom, min(GoogleStaticMapGenerater.ZOOM_RANGE), max(GoogleStaticMapGenerater.ZOOM_RANGE)))

        if settings.scale is not None and settings.scale not in GoogleStaticMapGenerater.SCALE_RANGE:
            raise ValueError(
                "[%s] is not a scale setting. Must be between %s and %s" %
                (settings.scale, min(GoogleStaticMapGenerater.SCALE_RANGE), max(GoogleStaticMapGenerater.SCALE_RANGE)))

        if settings.format not in GoogleStaticMapGenerater.FORMATS:
            raise ValueError(
                "[%s] is not a valid file format. Valid formats include %s" %
                (settings.format, GoogleStaticMapGenerater.FORMATS))

        if settings.maptype not in GoogleStaticMapGenerater.MAPTYPES:
            raise ValueError(
                "[%s] is not a valid map type. Valid types include %s" %
                (settings.maptype, GoogleStaticMapGenerater.MAPTYPES))

    @property
    def settings(self):
        raise NotImplementedError('subclasses of GoogleStaticMapGeneraterGenerater must provide a settings method')

    @property
    def generate_url(self):
        raise NotImplementedError('subclasses of GoogleStaticMapGeneraterGenerater must provide a generate_url method')

