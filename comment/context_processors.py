# -*- coding: utf-8 -*-
from comment.models import Comment
from django.conf import settings

def latestcomments(request):
    lastcomments = []
    objects = []
    for c in Comment.objects.all().order_by('-date_publication'):
        a = c.get_article()
        s = c.get_sortie()
        if a and a not in objects:
            lastcomments.append(c)
            objects.append(a)
        if s and s not in objects:
            lastcomments.append(c)
            objects.append(s)
             
    return {'latestcomments': lastcomments[:settings.NAV_MAX_SIZE],}
