from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='resume')
@stringfilter
def resume(value):
    return "%s</p>" % value.split("</p>")[0]

@register.inclusion_tag('core/pagination_entry.html', takes_context=True)
def pagination_entry(context, paginator, objects_pagination):
    """
    Renders a pagination entry.
    """
    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'MEDIA_SERIAL': settings.MEDIA_SERIAL,
        'paginator': paginator,
        'objects_pagination': objects_pagination,
    }

@register.inclusion_tag('core/loading.html', takes_context=False)
def loading():
    """
    Renders a loading div
    """
    return {
        'MEDIA_URL'   : settings.MEDIA_URL,
        'MEDIA_SERIAL': settings.MEDIA_SERIAL,
    }
