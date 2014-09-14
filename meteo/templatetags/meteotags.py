from django import template
from django.conf import settings
from meteo.models import Prevision
import datetime

register = template.Library()

@register.inclusion_tag('meteo/previ_resume_entry.html', takes_context=True)
def previ_resume_entry(context, previ, color):
    """
    Renders a prevision resume entry.
    """
    user = context.get('user', None)
    perms = context.get('perms', None)

    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'MEDIA_SERIAL': settings.MEDIA_SERIAL,
        'previ': previ,
        'color': color,
        'user': user,
        'perms': perms,
    }

@register.inclusion_tag('meteo/previ_encart.html', takes_context=True)
def previ_encart(context, previsions):
    """
    Renders a prevision for a date.
    """
    user = context.get('user', None)
    perms = context.get('perms', None)

    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'MEDIA_SERIAL': settings.MEDIA_SERIAL,
        'previsions': previsions,
        'user': user,
        'perms': perms,
    }
