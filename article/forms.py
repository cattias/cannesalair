"""
Forms for article
"""
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.contrib.auth.models import User
from core.widgets import TextareaTiny, MediumTextInput
from article.models import Article
from article.views import internal_view_article
from account.decorators import login_required
from django.contrib.auth.decorators import permission_required
from log.models import LogActivity
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from core.mail import internal_sendmail, add_to_maillist
from account.models import Profil
import threading
from account.decorators import profil_required

class ArticleForm(forms.ModelForm):
    auteur = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
    titre = forms.CharField(required=True, label='Titre', widget=MediumTextInput)
    contenu = forms.CharField(required=True, label='Contenu', widget=TextareaTiny(attrs={'rows':'30', 'cols':'100'}))
    tags = forms.CharField(required=False, label='Tags', widget=MediumTextInput)
    class Meta:
        model = Article
        exclude = ['comments', 'titre_slug']

@login_required
@permission_required('article.add_article')
def create_new_article(request, template_name='article/article_add.html'):
    if request.method == 'POST': # If the form has been submitted...
        preview = request.POST.get('preview', None)
        editpreview = request.POST.get('editpreview', None)
        new_form = ArticleForm(request.POST)
        if not editpreview and new_form.is_valid():
            new_article = new_form.save(commit=False)
            if not preview:
                new_article.save()
                new_article.generate_slug()
                LogActivity.recordActivity(qui=request.user, quoi=new_article, comment="a publi&eacute; un nouvel article : <a href='%s'>%s</a>" % (new_article.get_absolute_url(), new_article.titre))
                subscribe_article(new_article.auteur.get_profile(), new_article)
                ThreadMail(new_article).start()
                # Redirect after POST
                return HttpResponseRedirect(new_article.get_absolute_url())
            else:
                return internal_view_article(request, new_article, urlretour=reverse("addarticle"))
        else:
            form = new_form
    else:
        init = {}
        init['auteur'] = request.user.pk
        form = ArticleForm(initial=init)
    return render_to_response(template_name,
                              RequestContext(request,
                                             {'form': form,
                                              'full': True,
                                              }))

def send_notification_new_article(article, template_name="article/mail_new_article.html"):
    current_site = Site.objects.get_current()
    site_name = current_site.name
    domain = current_site.domain
    maillist = []
        
    for p in Profil.objects.filter(suivre_les_articles=True):
        add_to_maillist(maillist, p.user, article.auteur)

    subject = "[CAL] %s" % (article.titre)
    from_email = "Les Cannes A L'air <no-reply@cannesalair.fr>"
    for u in maillist:
        text = render_to_string(template_name, {'site_name': site_name,
                                                'domain': domain,
                                                'user': article.auteur,
                                                'article': article,
                                                'profil': u,
                                                })
        internal_sendmail(u.email, from_email, text, subject)

class ThreadMail(threading.Thread):
    def __init__(self, article):
        threading.Thread.__init__(self)
        self.article = article
        
    def run(self):
        send_notification_new_article(self.article)

@login_required
@permission_required('article.add_article')
def edit_article(request, slug, template_name='article/article_edit.html'):
    article = Article.objects.get(titre_slug=slug)
    if request.method == 'POST': # If the form has been submitted...
        preview = request.POST.get('preview', None)
        editpreview = request.POST.get('editpreview', None)
        new_form = ArticleForm(request.POST, instance=article)
        if not editpreview and new_form.is_valid():
            new_article = new_form.save(commit=False)
            if not preview:
                new_article.save()
                new_article.generate_slug()
                LogActivity.recordActivity(qui=request.user, quoi=new_article, comment="a modifi&eacute; l'article : <a href='%s'>%s</a>" % (article.get_absolute_url(), article.titre))
                # Redirect after POST
                return HttpResponseRedirect(article.get_absolute_url())
            else:
                return internal_view_article(request, new_article, urlretour=reverse("editarticle", kwargs={'slug': slug}))
        else:
            form = new_form
    else:
        form = ArticleForm(instance=article)

    return render_to_response(template_name,
                              RequestContext(request,
                                             {'form': form,
                                              'full': True,
                                              'article': article,
                                              }))

@login_required
@permission_required('article.delete_article')
def delete_article(request, slug):
    article = Article.objects.get(titre_slug=slug)
    if article:
        article.delete()
    return HttpResponseRedirect(reverse("articles"))

@login_required
@profil_required
def subscribe_article_slug(request, slug):
    a = Article.objects.get(titre_slug=slug)
    subscribe_article(request.user.get_profile(), a)
    return HttpResponseRedirect(a.get_absolute_url())

def subscribe_article(profile, article):
    if profile and article not in profile.articles.all():
        profile.articles.add(article)

@login_required
@profil_required
def unsubscribe_article_slug(request, slug):
    a = Article.objects.get(titre_slug=slug)
    unsubscribe_article(request.user.get_profile(), a)
    next_page = request.GET.get('next_page')
    if next_page:
        return HttpResponseRedirect(next_page)
    else:
        return HttpResponseRedirect(a.get_absolute_url())

def unsubscribe_article(profile, article):
    if profile and article in profile.articles.all():
        profile.articles.remove(article)
