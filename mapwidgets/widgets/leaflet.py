from django.forms import Media

from mapwidgets.settings import mw_settings
from mapwidgets.widgets.base import BasePointFieldWidget


class LeafletPointFieldWidget(BasePointFieldWidget):
    template_name = 'mapwidgets/pointfield/leaflet/interactive_widget.html'
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
            'mapwidgets/js/mw_init.js',
            'mapwidgets/js/mw_jquery_class.js',
            'mapwidgets/js/pointfield/interactive/mw_pointfield_base.js',
            'mapwidgets/js/pointfield/interactive/leaflet/mw_pointfield.js',
        ]

        return Media(js=js, css=css)
