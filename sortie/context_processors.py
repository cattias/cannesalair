# -*- coding: utf-8 -*-
from sortie.models import Sortie, Participant
from django.conf import settings
import datetime

def latestsorties(request):
    return {'latestsorties': Sortie.objects.all().order_by('-date_debut')[:settings.NAV_MAX_SIZE],}

def sortiesavenir(request):
    now = datetime.datetime.now()
    now = now - datetime.timedelta(days=1)
    sortiesavenir = Sortie.objects.filter(date_fin__gte=now).order_by('date_debut')
    return {'sortiesavenir': sortiesavenir,}

def allparticipants(request):
    return {'allparticipants': Participant.objects.all().order_by('-date_update')[:settings.NAV_MAX_SIZE],}

