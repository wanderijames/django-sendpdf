"""You have to set BASE_DIR = os.path.dirname(os.path.dirname(__file__)) in django.conf.settings and in  load pdftags in your templates"""
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
