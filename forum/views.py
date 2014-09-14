# -*- coding: utf-8 -*-
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from forum.models import Thread, Forum, Groupe
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse

def list_groupes(request, template_name='forum/groupe_list.html'):
    return render_to_response(template_name,
                              context_instance=RequestContext(request,
                                             {'groupes': Groupe.objects.all().order_by('ordre'),}))

def show_forum(request, slug, template_name='forum/show_forum.html'):
    try:
        f = Forum.objects.get(titre_slug=slug)
    except Forum.DoesNotExist:
        try:
            f = Forum.objects.get(pk=int(slug))
        except ValueError, Forum.DoesNotExist:
            raise Http404("La discussion '%s' n'existe pas!" % slug)
    return render_to_response(template_name,
                              context_instance=RequestContext(request,
                                             {'f': f,
                                              'threads': f.forum_thread_set.order_by('-date_creation'),
                                              }))

def show_thread(request, slug, template_name='forum/show_thread.html'):
    try:
        t = Thread.objects.get(titre_slug=slug)
    except Thread.DoesNotExist:
        try:
            t = Thread.objects.get(pk=int(slug))
        except ValueError:
            return HttpResponseRedirect(reverse("groupes"))
    return internal_view_thread(request, t)

def internal_view_thread(request, thread, template_name='forum/show_thread.html', urlretour=None, messagesuppl=None):
    issubscribed = False
    if request.user.is_authenticated() and thread.pk:
        issubscribed = request.user.get_profile() in thread.discussions_suivies_set.all()
    messages = [m for m in thread.thread_message_set.all().order_by('date_publication')] if thread.pk else []
    if messagesuppl:
        messages.append(messagesuppl)
        
    contenu = None
    if request.POST:
        contenu = request.POST.get('contenu')
        
    return render_to_response(template_name,
                              RequestContext(request,
                                             {'thread': thread,
                                              'listmessages': messages,
                                              'full': True,
                                              'urlretour': urlretour,
                                              'messagesuppl': messagesuppl,
                                              'issubscribed': issubscribed,
                                              'contenu': contenu,
                                              }))
