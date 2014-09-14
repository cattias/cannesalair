# -*- coding: utf-8 -*-
from forum.models import Message
from django.conf import settings

def latestmessages(request):
    lastmessages = []
    ts = []
    for m in Message.objects.all().order_by('-date_publication'):
        if m.thread not in ts:
            lastmessages.append(m)
            ts.append(m.thread)
    return {'latestmessages': lastmessages[:settings.NAV_MAX_SIZE],}
