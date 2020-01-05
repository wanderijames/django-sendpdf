import os
from django import template
register = template.Library()

_DIR = os.path.abspath(os.path.dirname(__file__))


@register.simple_tag
def pdf_static(static_url, pdf=None):
    if pdf is not None:
        file = os.path.join(
            _DIR,
            os.pardir,
            "static",
            static_url
        )
        return file
    return "/static/{}".format(static_url)
