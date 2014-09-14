# -*- coding: utf-8 -*-
from article.models import Article, ArticleOldSlugs
from django.http import Http404
from django.template.context import RequestContext
from django.shortcuts import render_to_response
import datetime
from django.contrib.auth.models import User

def list_articles(request, type='article', template_name='article/article_list.html'):
    articles = Article.objects.all()
    if type == 'article':
        articles = articles.exclude(tags__icontains="accueil").exclude(tags__icontains="lien")
    if type == 'accueil':
        articles = articles.filter(tags__icontains="accueil")
    if type == 'lien':
        articles = articles.filter(tags__icontains="lien")
    articles = articles.order_by('-date_publication')
    years = []
    for a in articles:
        if not a.date_publication.year in years:
            years.append(a.date_publication.year)
    year = request.GET.get("year", None)

    tags = request.GET.getlist('tag')
    if tags:
        for t in tags:
            articles = articles.filter(tags__icontains=t)
            
    auteur = request.GET.get('auteur')
    if auteur:
        try:
            auteur = User.objects.get(pk=int(auteur))
            articles = articles.filter(auteur=auteur)
        except:
            pass

    if not tags and not auteur:
        if not year:
            year = datetime.date.today().year
        else:
            year = int(year)
        articles = articles.filter(date_publication__year=year)

    articlescount = 0
    try:
        articlescount = articles.count()
    except:
        pass
    return render_to_response(template_name,
                              RequestContext(request,
                                             {'articles': articles,
                                              'tags': tags,
                                              'years': years,
                                              'year': year,
                                              'auteur': auteur,
                                              'articlescount': articlescount,
                                              }))


def view_article(request, slug, template_name='article/article_view.html'):
    try:
        article = Article.objects.get(titre_slug=slug)
    except Article.DoesNotExist:
        try:
            article = Article.objects.get(pk=int(slug))
        except:
            try:
                old = ArticleOldSlugs.objects.get(titre_slug=slug)
                if old:
                    article = old.article
                else:
                    raise Http404("L'article n'existe pas")
            except ArticleOldSlugs.DoesNotExist:
                raise Http404("L'article n'existe pas")
    return internal_view_article(request, article, template_name)

def internal_view_article(request, article, template_name='article/article_view.html', urlretour=None):
    date_publication = article.date_publication if article.date_publication else datetime.datetime.now()
    canbeedited = not urlretour and (request.user == article.auteur or request.user.is_superuser)
    issubscribed = False
    if request.user.is_authenticated() and article.pk:
        issubscribed = request.user.get_profile() in article.articles_suivis_set.all()
    return render_to_response(template_name, RequestContext(request, 
                                                            {'article': article,
                                                             'date_publication': date_publication,
                                                             'urlretour': urlretour,
                                                             'canbeedited': canbeedited,
                                                             'issubscribed': issubscribed,
                                                             'full': True,
                                                             }))

def accueil(request, template_name='article/accueil.html'):
    allarticles = Article.objects.all()
    allarticles = allarticles.exclude(tags__icontains="accueil").exclude(tags__icontains="lien")
    allarticles = allarticles.order_by('-date_publication')
    years = []
    for a in allarticles:
        if not a.date_publication.year in years:
            years.append(a.date_publication.year)
    year = request.GET.get("year", None)
    if not year:
        year = datetime.date.today().year
    else:
        year = int(year)
    articles = allarticles.filter(date_publication__year=year)
    articlescount = articles.count()
    if allarticles.count() > 0:
        while articlescount == 0:
            year = year - 1
            articles = allarticles.filter(date_publication__year=year)
            articlescount = articles.count()

    return render_to_response(template_name,
                              RequestContext(request,
                                             {'articles': articles,
                                              'years': years,
                                              'year': year,
                                              'articlescount': articlescount,
                                              }))

def about(request, template_name='article/about.html'):
    article = Article.objects.filter(tags__icontains="accueil").order_by("pk")[0]
    return render_to_response(template_name, RequestContext(request, 
                                                            {'article': article,
                                                             'full': True,
                                                             }))
