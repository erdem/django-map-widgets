from django.utils.safestring import mark_safe
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text


def html_escape(html):
    """Return the given HTML with ampersands, quotes and carets encoded."""
    return mark_safe(force_text(html).replace('&', '&amp;')
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
