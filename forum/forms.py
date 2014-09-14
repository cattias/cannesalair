# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from account.decorators import login_required
from account.models import Profil
from forum.models import Thread, Message, Forum
from django import forms
from core.widgets import TextareaTiny, MediumTextInput
from account.decorators import profil_required
from django.template.loader import render_to_string
from log.models import LogActivity
from core.mail import internal_sendmail, add_to_maillist
from forum.views import internal_view_thread
import datetime
import threading

class ThreadForm(forms.ModelForm):
    titre = forms.CharField(required=True, label='Titre', widget=MediumTextInput)
    forum = forms.ModelChoiceField(queryset=Forum.objects.all(), widget=forms.HiddenInput)

    class Meta:
        model = Thread
        exclude = ['titre_slug']

class MessageForm(forms.ModelForm):
    contenu = forms.CharField(required=True, label='Message', widget=TextareaTiny(attrs={'rows':'30', 'cols':'100'}))
    auteur = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
    
    class Meta:
        model = Message
        exclude = ['thread', 'titre_slug']

@login_required
@profil_required
def new_thread(request, slug, template_name="forum/new_thread_form.html"):
    forum = Forum.objects.get(titre_slug=slug)
    
    if request.POST:
        preview = request.POST.get('preview', None)
        editpreview = request.POST.get('editpreview', None)
        new_threadform = ThreadForm(request.POST)
        new_messageform = MessageForm(request.POST)
        if not editpreview and new_threadform.is_valid() and new_messageform.is_valid():
            contenu = request.POST.get('contenu')
            newthread = new_threadform.save(commit=False)
            if not preview:
                newthread.save()
                newthread.generate_slug()
                create_message(auteur=request.user, contenu=contenu, thread=newthread, isnewthread=True)
                return HttpResponseRedirect(newthread.get_absolute_url())
            else:
                newmessage = Message(auteur=request.user, contenu=contenu, date_publication=datetime.datetime.now())
                return internal_view_thread(request, newthread, urlretour=reverse("newthread", kwargs={"slug":slug}), messagesuppl=newmessage)
        else:
            threadform = new_threadform
            messageform = new_messageform
    else:
        threadform = ThreadForm(initial={"forum":forum.pk})
        messageform = MessageForm(initial={"auteur":request.user.pk})

    context = RequestContext(request, {
        'forum': forum,
        'full': True,
        'threadform': threadform,
        'messageform': messageform,
    })
    
    return render_to_response(template_name, context)

def testmessagemail(request, message_key, template_name="forum/new_thread_mail.html"):
    message = Message.objects.get(pk=message_key)
    current_site = Site.objects.get_current()
    site_name = current_site.name
    domain = current_site.domain
    context = RequestContext(request, {
         'site_name': site_name,
         'domain': domain,
         'user': message.auteur,
         'message': message,
    })
    
    return render_to_response(template_name, context)

def send_message_mail(message, template_name="forum/message_mail.html"): 
    current_site = Site.objects.get_current()
    site_name = current_site.name
    domain = current_site.domain
    maillist = []
    for p in message.thread.discussions_suivies_set.all():
        add_to_maillist(maillist, p.user, message.auteur)
    for p in message.thread.forum.forums_suivis_set.all():
        add_to_maillist(maillist, p.user, message.auteur)
    for u in message.thread.forum.moderateurs.all():
        add_to_maillist(maillist, u, message.auteur)
        
    subject = "[Forum CAL] %s" % (message.thread.titre)
    from_email = "Les Cannes A L'air <no-reply@cannesalair.fr>"
    for u in maillist:
        text = render_to_string(template_name, {'site_name': site_name,
                                                'domain': domain,
                                                'user': message.auteur,
                                                'message': message,
                                                'profil': u,
                                                })
        internal_sendmail(u.email, from_email, text, subject)

@login_required
@profil_required
def new_message(request, slug, template_name="forum/new_message_form.html"):
    thread = Thread.objects.get(titre_slug=slug)
    if request.POST:
        preview = request.POST.get('preview', None)
        editpreview = request.POST.get('editpreview', None)
        messageform = MessageForm(request.POST)
        if not editpreview and messageform.is_valid():
            contenu = request.POST.get('contenu')
            if not preview:
                create_message(auteur=request.user, contenu=contenu, thread=thread)
            else:
                newmessage = Message(auteur=request.user, contenu=contenu, date_publication=datetime.datetime.now())
                return internal_view_thread(request, thread, urlretour=thread.get_absolute_url(), messagesuppl=newmessage)
    
    return HttpResponseRedirect("%s#commentaires-posting" % thread.get_absolute_url())

def send_notification_new_thread(message, template_name="forum/new_thread_mail.html"):
    current_site = Site.objects.get_current()
    site_name = current_site.name
    domain = current_site.domain
    maillist = []
        
    for p in Profil.objects.filter(suivre_les_discussions=True):
        add_to_maillist(maillist, p.user, message.auteur)

    subject = "[Forum CAL] %s" % (message.thread.titre)
    from_email = "Les Cannes A L'air <no-reply@cannesalair.fr>"
    for u in maillist:
        text = render_to_string(template_name, {'site_name': site_name,
                                                'domain': domain,
                                                'user': message.auteur,
                                                'message': message,
                                                'profil': u,
                                                })
        internal_sendmail(u.email, from_email, text, subject)

def create_message(auteur, contenu, thread, isnewthread=False):
    newmessage = Message(auteur=auteur, contenu=contenu, thread=thread)
    newmessage.save()
    LogActivity.recordActivity(qui=auteur, quoi=newmessage, comment="a publi&eacute; un nouveau message : <a href='%s'>%s</a>" % (newmessage.thread.get_absolute_url(), newmessage.thread.titre))
    subscribe_thread_message(newmessage)
    ThreadMail(message=newmessage, isnewthread=isnewthread).start()
    return newmessage

class ThreadMail(threading.Thread):
    def __init__(self, message, isnewthread):
        threading.Thread.__init__(self)
        self.message = message
        self.isnewthread = isnewthread
        
    def run(self):
        if self.isnewthread:
            send_notification_new_thread(message=self.message)
        else:
            send_message_mail(message=self.message)

def subscribe_thread_message(message):
    p = message.auteur.get_profile()
    if p and message.thread not in p.discussions.all():
        p.discussions.add(message.thread)

@login_required
@profil_required
def subscribe_forum(request, slug):
    user = request.user
    p = user.get_profile()
    f = Forum.objects.get(titre_slug=slug)
    p.forums.add(f)
    return HttpResponseRedirect(f.get_absolute_url())

@login_required
@profil_required
def unsubscribe_forum(request, slug):
    user = request.user
    p = user.get_profile()
    f = Forum.objects.get(titre_slug=slug)
    p.forums.remove(f)
    return HttpResponseRedirect(f.get_absolute_url())

@login_required
@profil_required
def subscribe_thread(request, slug):
    user = request.user
    p = user.get_profile()
    t = Thread.objects.get(titre_slug=slug)
    p.discussions.add(t)
    return HttpResponseRedirect(t.get_absolute_url())

@login_required
@profil_required
def unsubscribe_thread(request, slug):
    user = request.user
    p = user.get_profile()
    t = Thread.objects.get(titre_slug=slug)
    p.discussions.remove(t)
    next_page = request.GET.get('next_page')
    if next_page:
        return HttpResponseRedirect(next_page)
    else:
        return HttpResponseRedirect(t.get_absolute_url())
