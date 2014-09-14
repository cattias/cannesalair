# -*- coding: utf-8 -*-
import urllib

def activetab(request):
    path = request.META.get('PATH_INFO')
    article = None
    galerie = None
    activite = None
    forum = None
    notif = None
    meteo = None
    
    if path:
        if path.find('article/') > 0:
            article = 'actif'
        elif path.find('sortie/') > 0:
            activite = 'actif'
        elif path.find('forum/') > 0:
            forum = 'actif'
        elif path.find('galerie/') > 0:
            galerie = 'actif'
        elif path.find('notification/') > 0:
            notif = 'actif'
        elif path.find('meteo/') > 0:
            meteo = 'actif'
       
    return {'tab_article': article, 'tab_galerie': galerie, 'tab_activite': activite, 'tab_forum': forum, 'tab_notification': notif, 'tab_meteo': meteo,}

def next_page(request):
    next_page = request.GET.get('next_page', None)
    next_query = request.GET.get('next_query', None)
    loginerror = None
    
    if not next_page:
        next_page = request.META.get('PATH_INFO')
        next_query = request.META.get('QUERY_STRING')
        loginerror = request.COOKIES.get('loginerror', None)
        
    if next_query:
        try:
            next_query = urllib.quote_plus(next_query)
        except:
            pass

    return {'next_query': next_query, 'next_page': next_page, 'loginerror': loginerror,}
