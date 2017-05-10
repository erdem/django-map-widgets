from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode


def html_escape(html):
    """Returns the given HTML with ampersands, quotes and carets encoded."""
    return mark_safe(force_unicode(html).replace('&', '&amp;')
                     .replace('<', '&lt;').replace('>', '&gt;')
                     .replace('"', '&quot;').replace("'", '&#39;')
                     )


def get_textarea_html(html_id, name, point):
    point_value = point.wkt if point else ''
    return '<textarea id="{html_id}" name="{name}">{point}</textarea>'.format(
        html_id=html_id,
        name=name,
        point=point_value
    )
