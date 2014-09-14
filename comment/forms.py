"""
Forms for comments
"""
from django import forms
from django.shortcuts import render_to_response
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth.models import User
from article.models import Article
from sortie.models import Sortie
from comment.models import Comment
from account.decorators import login_required
from django.template.loader import render_to_string
from core.mail import internal_sendmail, add_to_maillist
from log.models import LogActivity
from article.forms import subscribe_article
from sortie.forms import subscribe_sortie
import threading
from galerie.models import Galerie
from galerie.views import subscribe_galerie
from meteo.models import Prevision

class CommentForm(forms.ModelForm):
    auteur = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
    contenu = forms.CharField(required=True, label='Contenu', widget=forms.Textarea(attrs={'rows':'4', 'cols':'50'}))
    class Meta:
        model = Comment


@login_required
def new_comment(request, pk, type, template_name='comment/new_comment_form.html'):
    article = None
    sortie = None
    galerie = None
    previ = None
    urlredirect = None
    if type == 'article':
        article = Article.objects.get(pk=pk)
        urlredirect = "%s#commentaires-posting" % article.get_absolute_url()
    if type == 'sortie':
        sortie = Sortie.objects.get(pk=pk)
        urlredirect = "%s#commentaires-posting" % sortie.get_absolute_url()
    if type == 'galerie':
        galerie = Galerie.objects.get(pk=pk)
        urlredirect = "%s#commentaires-posting" % galerie.get_absolute_url()
    if type == 'previ':
        previ = Prevision.objects.get(pk=pk)
        urlredirect = "%s#commentaires-posting" % previ.get_absolute_url()
        
    if request.method == 'POST': # If the form has been submitted...
        new_form = CommentForm(request.POST)
        if new_form.is_valid():
            new_comment = new_form.save(commit=False)
            new_comment.save()
            if article:
                article.comments.add(new_comment)
                subscribe_article_comment(new_comment, article)
                LogActivity.recordActivity(qui=request.user, quoi=new_comment, comment="a post&eacute; un nouveau commentaire au sujet de l'article : <a href='%s'>%s</a>" % (article.get_absolute_url(), article.titre), surquoi=article)
            if sortie:
                sortie.comments.add(new_comment)
                subscribe_sortie_comment(new_comment, sortie)
                LogActivity.recordActivity(qui=request.user, quoi=new_comment, comment="a post&eacute; un nouveau commentaire au sujet de l'activit&eacute; : <a href='%s'>%s</a>" % (sortie.get_absolute_url(), sortie.titre), surquoi=sortie)
            if galerie:
                galerie.comments.add(new_comment)
                subscribe_galerie_comment(new_comment, galerie)
                LogActivity.recordActivity(qui=request.user, quoi=new_comment, comment="a post&eacute; un nouveau commentaire au sujet de la galerie : <a href='%s'>%s</a>" % (galerie.get_absolute_url(), galerie.titre), surquoi=galerie)
            if previ:
                previ.comments.add(new_comment)
                LogActivity.recordActivity(qui=request.user, quoi=new_comment, comment="a post&eacute; un nouveau commentaire au sujet de la pr&eacute;vision : <a href='%s'>%s</a>" % (previ.get_absolute_url(), previ), surquoi=previ)
            ThreadMail(new_comment).start()
        # Redirect after POST
        return HttpResponseRedirect(urlredirect)
    else:
        init = {}
        init['auteur'] = request.user.pk
        form = CommentForm(initial=init)
    return render_to_response(template_name,
                              RequestContext(request,
                                             {'form': form,
                                              'type': type,
                                              'pk': pk,
                                              }))

def subscribe_article_comment(comment, article):
    p = comment.auteur.get_profile()
    subscribe_article(p, article)

def subscribe_sortie_comment(comment, sortie):
    p = comment.auteur.get_profile()
    subscribe_sortie(p, sortie)

def subscribe_galerie_comment(comment, galerie):
    p = comment.auteur.get_profile()
    subscribe_galerie(p, galerie)

@login_required
def delete_comment(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    article = comment.get_article()
    sortie = comment.get_sortie()
    galerie = comment.get_galerie()
    if article:
        urlredirect = "%s#commentaires-posting" % article.get_absolute_url()
    if sortie:
        urlredirect = "%s#commentaires-posting" % sortie.get_absolute_url()
    if galerie:
        urlredirect = "%s#commentaires-posting" % galerie.get_absolute_url()
    if comment:
        comment.delete()
    return HttpResponseRedirect(urlredirect)

def send_comment_mail(comment): 
    current_site = Site.objects.get_current()
    site_name = current_site.name
    domain = current_site.domain
    maillist = []
    article = None
    sortie = None
    galerie = None
    from_email = "Les Cannes A L'air <no-reply@cannesalair.fr>"

    for s in comment.sortie_comments_set.all():
        sortie = s
        for p in sortie.sorties_suivies_set.all():
            add_to_maillist(maillist, p.user, comment.auteur)

    for a in comment.article_comments_set.all():
        article = a
        for p in article.articles_suivis_set.all():
            add_to_maillist(maillist, p.user, comment.auteur)

    for g in comment.galerie_comments_set.all():
        galerie = g
        for p in galerie.galeries_suivies_set.all():
            add_to_maillist(maillist, p.user, comment.auteur)

    template_name=None
    if article:
        subject = "[CAL] %s" % (article.titre)
        template_name="comment/message_mail_article.html"
    if sortie:
        subject = "[CAL](%s) %s" % (sortie.get_short_date_string(), sortie.titre)
        template_name="comment/message_mail_sortie.html"
    if galerie:
        subject = "[CAL] %s" % (galerie.titre)
        template_name="comment/message_mail_galerie.html"
    for u in maillist:
        text = render_to_string(template_name, {'site_name': site_name,
                                                'domain': domain,
                                                'user': comment.auteur,
                                                'comment': comment,
                                                'profil':u,
                                                'sortie': sortie,
                                                'article': article,
                                                'galerie': galerie,
                                                })
        internal_sendmail(u.email, from_email, text, subject)

class ThreadMail(threading.Thread):
    def __init__(self, comment):
        threading.Thread.__init__(self)
        self.comment = comment
        
    def run(self):
        send_comment_mail(self.comment)
