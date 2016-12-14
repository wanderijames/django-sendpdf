"""You have to set BASE_DIR = os.path.dirname(os.path.dirname(__file__)) in django.conf.settings and in  load pdftags in your templates"""
import os
from django.conf import settings
from django import template
register = template.Library()


@register.simple_tag
def pdf_static(static_url, pdf=None):
    if pdf is not None:
        return os.path.join(settings.BASE_DIR, "sendpdf/static/{}".format(static_url))
    return "/static/{}".format(static_url)
