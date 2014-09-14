from django import template
from photologue.models import Gallery
from django.conf import settings

register = template.Library()

@register.simple_tag
def next_in_gallery(photo, gallery):
    next = photo.get_next_in_gallery(gallery)
    if next:
        return '<a title="%s" href="%s"><img src="%s"/></a>' % (next.title, next.get_absolute_url(), next.get_thumbnail_url())
    return ""
    
@register.simple_tag
def previous_in_gallery(photo, gallery):
    prev = photo.get_previous_in_gallery(gallery)
    if prev:
        return '<a title="%s" href="%s"><img src="%s"/></a>' % (prev.title, prev.get_absolute_url(), prev.get_thumbnail_url())
    return ""

@register.inclusion_tag('photologue/gallery_entry.html', takes_context=True)
def gallery_entry(context, gallery):
    """
    Renders a gallery entry.
    """
    user = context.get('user', None)
    
    show_count = True
    count = 0

    if show_count:
        count = gallery.photos.all().count()

    selected = False
    object = context.get('object', None)
    if object and type(object) == Gallery:
        selected = object.pk == gallery.pk
    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'MEDIA_SERIAL': settings.MEDIA_SERIAL,
        'g': gallery,
        'count': count,
        'show_count': show_count,
        'user': user,
        'selected': selected,
    }

@register.inclusion_tag('photologue/allgalleries_entry.html', takes_context=True)
def allgalleries_entry(context):
    """
    Renders a gallery entry.
    """
    user = context.get('user', None)
    
    show_count = True
    count = 0

    if show_count:
        count = Gallery.objects.all().count()

    selected = False
    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'MEDIA_SERIAL': settings.MEDIA_SERIAL,
        'count': count,
        'show_count': show_count,
        'user': user,
        'selected': selected,
    }
