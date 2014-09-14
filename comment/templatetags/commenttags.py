from comment.forms import CommentForm
from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('comment/new_comment_form.html', takes_context=True)
def new_comment_form(context, type, pk):
    """
    Renders a tags entry.
    """
    user = context.get('user', None)
    init = {}
    init['auteur'] = user.pk
    form = CommentForm(initial=init)
    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'MEDIA_SERIAL': settings.MEDIA_SERIAL,
        'user': user,
        'type': type,
        'pk': pk,
        'form': form,
    }

@register.inclusion_tag('comment/comments_entry.html', takes_context=True)
def comments_entry(context, type, pk, comments):
    """
    Renders a tags entry.
    """
    user = context.get('user', None)

    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'MEDIA_SERIAL': settings.MEDIA_SERIAL,
        'type': type,
        'pk': pk,
        'comments': comments,
        'user': user,
    }
