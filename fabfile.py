from fabric.api import local


JS_FILE_MAPPING = {
    "GooglePointFieldWidget": {
        "input_files": [
            "mapwidgets/static/mapwidgets/js/jquery_class.js",
            "mapwidgets/static/mapwidgets/js/django_mw_base.js",
            "mapwidgets/static/mapwidgets/js/mw_google_point_field.js",

        ],
        "output_file": "mapwidgets/static/mapwidgets/js/mw_google_point_field.min.js"
    },
    "GooglePointFieldInlineWidget": {
        "input_files": [
            "mapwidgets/static/mapwidgets/js/jquery_class.js",
            "mapwidgets/static/mapwidgets/js/django_mw_base.js",
            "mapwidgets/static/mapwidgets/js/mw_google_point_field.js",
            "mapwidgets/static/mapwidgets/js/mw_google_point_field_generater.js",
        ],
        "output_file": "mapwidgets/static/mapwidgets/js/mw_google_point_inline_field.min.js"
    }
}


def minify_js_files():
    """
        This command minified js files with UglifyJS
    """
    for k, v in JS_FILE_MAPPING.items():
        input_files = " ".join(v["input_files"])
        output_file = v["output_file"]

        uglifyjs_command = "uglifyjs {input_files} -o {output_file}".format(
            input_files=input_files,
            output_file=output_file
        )
        local(uglifyjs_command)
