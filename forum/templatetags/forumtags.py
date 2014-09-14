from django import template
from django.conf import settings
from forum.models import Message

register = template.Library()

@register.inclusion_tag('forum/forums_entry.html', takes_context=True)
def forums_entry(context, forum):
    """
    Renders a forum entry.
    """
    user = context.get('user', None)
    totalthreads = 0
    totalmessages = 0
    derniermessage = None
    for t in forum.forum_thread_set.all():
        totalthreads += 1
        for m in t.thread_message_set.all():
            if not derniermessage:
                derniermessage = m
            if m.date_publication > derniermessage.date_publication:
                derniermessage = m
            totalmessages += 1
    
    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'MEDIA_SERIAL': settings.MEDIA_SERIAL,
        'f': forum,
        'user': user,
        'moderateurs': forum.moderateurs.all(),
        'totalthreads': totalthreads,
        'totalmessages': totalmessages,
        'derniermessage': derniermessage,
    }

@register.inclusion_tag('forum/threads_entry.html', takes_context=True)
def threads_entry(context, thread):
    """
    Renders a forum entry.
    """
    user = context.get('user', None)
    totalreponses = thread.thread_message_set.count() - 1
    auteur = thread.thread_message_set.all().order_by('date_publication')[0].auteur
    derniermessage = thread.thread_message_set.all().order_by('-date_publication')[0]
    
    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'MEDIA_SERIAL': settings.MEDIA_SERIAL,
        't': thread,
        'user': user,
        'auteur': auteur,
        'totalreponses':totalreponses,
        'derniermessage':derniermessage,
    }

@register.inclusion_tag('forum/messages_entry.html', takes_context=True)
def messages_entry(context, message):
    """
    Renders a forum entry.
    """
    user = context.get('user', None)
    rang = message.thread.thread_message_set.filter(date_publication__lt=message.date_publication).count()+1
    messagescount = Message.objects.all().filter(auteur=message.auteur).count()
    p = message.auteur.get_profile()

    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'MEDIA_SERIAL': settings.MEDIA_SERIAL,
        'm': message,
        'rang': rang,
        'user': user,
        'messagescount': messagescount,
        'p': p,
    }

@register.inclusion_tag('forum/pagination_entry.html', takes_context=True)
def pagination_entry(context, objects_pagination):
    """
    Renders a pagination entry.
    """
    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'MEDIA_SERIAL': settings.MEDIA_SERIAL,
        'objects_pagination': objects_pagination,
    }
