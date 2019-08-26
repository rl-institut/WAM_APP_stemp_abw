from django import template
from stemp_abw.app_settings import LANGUAGE_STORE

register = template.Library()


@register.simple_tag
def language_store():
    return LANGUAGE_STORE
