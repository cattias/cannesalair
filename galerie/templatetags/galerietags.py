from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('galerie/apercu_galerie.html', takes_context=True)
def apercu_galerie(context, galerie):
    """
    Renders a apercu de galerie.
    """
    images = galerie.photos_set.all()[:3]
    MEDIA_URL = settings.MEDIA_URL
    
    return {
        'images': images,
        'galerie': galerie,
        'MEDIA_URL': MEDIA_URL,
    }
