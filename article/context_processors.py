# -*- coding: utf-8 -*-
from tagging.models import Tag
from article.models import Article, Lien
from django.conf import settings

def alltags(request):
    return {'alltags': Tag.objects.exclude(name="avatar"),}

def latestarticles(request):
    return {'latestarticles': Article.objects.all().order_by('-date_publication')[:settings.NAV_MAX_SIZE],}

def allliens(request):
    return {'allliens': Lien.objects.exclude(disabled=True).order_by('ordre'),}
