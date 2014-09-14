# -*- coding: utf-8 -*-
from log.models import LogActivity
from sortie.models import Participant
from django.contrib.contenttypes.models import ContentType

def notifications(request):
    new_notification = None
    if request.user.is_authenticated():
        last_known_activity = 0
        if request.user.get_profile().last_known_activity:
            last_known_activity = request.user.get_profile().last_known_activity.pk
        new_notification = LogActivity.objects.exclude(qui=request.user).exclude(type=ContentType.objects.get_for_model(Participant)).filter(pk__gt=last_known_activity).count()
        if new_notification == 0:
            new_notification = None
    return {'new_notification': new_notification,}
