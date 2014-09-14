# -*- coding: utf-8 -*-
from photologue.models import Gallery
from django.conf import settings

def allgalleries(request):
    return {'allgalleries': Gallery.objects.filter(is_public=True).order_by('-date_added')[:settings.NAV_MAX_SIZE],}

