from django import VERSION
from django.templatetags.static import static
from django.utils.html import format_html, html_safe, mark_safe

from mapwidgets.settings import mw_settings

__all__ = ("AsyncJS", "static")


class AsyncJS:
    """ """

    def __init__(self, js):
        self.js = js

    def startswith(self, _):
        # Masquerade as absolute path so that we are returned as-is.
        return True

    def __repr__(self):
        return f"AsyncJS({self.js})"

    if VERSION >= (4, 1):

        def __str__(self):
            return format_html(
                '<script async src="{}"></script>',
                (
                    self.js
                    if self.js.startswith(("http://", "https://", "/"))
                    else static(self.js)
                ),
            )

    else:

        def __html__(self):
            return format_html(
                '<script async src="{}"></script>',
                (
                    self.js
                    if self.js.startswith(("http://", "https://", "/"))
                    else static(self.js)
                ),
            )

    def __eq__(self, other):
        return self.js == other

    def __hash__(self):
        return hash((self.js))


if VERSION >= (4, 1):
    AsyncJS = html_safe(AsyncJS)


def minify_if_not_debug(asset):
    """
    Transform template string `asset` by inserting '.min' if DEBUG=False
    """
    return asset.format("" if not mw_settings.MINIFED else ".min")
