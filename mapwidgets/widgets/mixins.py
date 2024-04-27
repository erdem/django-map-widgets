import json


class PointFieldInlineWidgetMixin:

    def get_js_widget_data(self, name, element_id):
        map_elem_selector = "#%s-mw-wrap" % name
        map_elem_id = "%s-map-elem" % name
        google_auto_input_id = "%s-mw-google-address-input" % name
        django_input_id = "#%s" % element_id
        js_widget_params = {
            "widgetWrapSelector": map_elem_selector,
            "mapId": map_elem_id,
            "googleAutoInputId": google_auto_input_id,
            "djangoInputId": django_input_id,
        }
        return js_widget_params

    def render(self, name, value, attrs=None, renderer=None):
        if not attrs:
            attrs = dict()

        element_id = attrs.get("id")
        is_formset_empty_form_template = "__prefix__" in name
        widget_data = self.get_js_widget_data(name, element_id)
        attrs.update(
            {
                "js_widget_data": json.dumps(widget_data),
                "is_formset_empty_form_template": is_formset_empty_form_template,
            }
        )
        self.as_super = super(PointFieldInlineWidgetMixin, self)
        if renderer is not None:
            return self.as_super.render(name, value, attrs, renderer)
        else:
            return self.as_super.render(name, value, attrs)
