from django.forms import Media

from mapwidgets.settings import mw_settings
from mapwidgets.widgets.base import BasePointFieldWidget


class LeafletPointFieldWidget(BasePointFieldWidget):
    template_name = 'mapwidgets/leaflet_point_field_widget.html'
    settings_namespace = 'mw_settings.Leaflet.PointField.interactive'
    settings = mw_settings.Leaflet.PointField.interactive

    @property
    def media(self):
        css = {
            'all': [
                'https://unpkg.com/leaflet@1.7.1/dist/leaflet.css',
                'mapwidgets/css/map_widgets.css',
            ]
        }
        js = [
            'https://unpkg.com/leaflet@1.7.1/dist/leaflet.js',
            'mapwidgets/js/jquery_init.js',
            'mapwidgets/js/jquery_class.js',
            'mapwidgets/js/django_mw_base.js',
            'mapwidgets/js/mw_leaflet_point_field.js',
        ]

        return Media(js=js, css=css)
