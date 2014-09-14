# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.template.context import RequestContext
from djblets.auth.util import internal_login
from account.models import Profil
import urllib
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from log.models import LogActivity
from django.contrib.contenttypes.models import ContentType
from sortie.models import Participant
from django.core.urlresolvers import reverse
from account.decorators import login_required

###########################
#       User Login        #
###########################

def login(request, next_page, next_query=None, template_name="accounts/login.html"):
    """Simple login form view which doesn't rely on Django's current
       inflexible oldforms-based auth view.
    """

    error = None
    if request.POST:
        request.session.set_test_cookie()
        loginbox = request.POST.get('loginbox')
        error = internal_login(request,
                               request.POST.get('username'),
                               request.POST.get('password'))
        urlnext = request.REQUEST.get("next_page", next_page)
        query = request.REQUEST.get("next_query", next_query)
        if query and not query == "None":
            try:
                urlnext += "?%s" % urllib.unquote_plus(query)
            except:
                pass
        if not error or loginbox:
            response = HttpResponseRedirect(urlnext)
            if error:
                response.set_cookie('loginerror',
                            value=error,
                            max_age='%s' % (5), # in seconds
                            path=settings.SITE_ROOT,
                            )
            else:
                response.delete_cookie('loginerror', path=settings.SITE_ROOT)
            return response

    request.session.set_test_cookie()
    context = RequestContext(request, {
        'error' : error,
        'login_url' : settings.LOGIN_URL,
        'full': True,
        'next_page' : request.REQUEST.get("next_page", next_page),
        'next_query' : request.REQUEST.get("next_query", next_query),
    })
    return render_to_response(template_name, context)

def logout(request, next_page=None, next_query=None, template_name='registration/logged_out.html', redirect_field_name=REDIRECT_FIELD_NAME):
    "Logs out the user and displays 'You are logged out' message."
    from django.contrib.auth import logout
    logout(request)

    urlnext = request.REQUEST.get("next_page", next_page)
    query = request.REQUEST.get("next_query", next_query)
    if query and not query == "None":
        urlnext += "?%s" % urllib.unquote_plus(query)
    return HttpResponseRedirect(urlnext)
    
@login_required
def view_profil(request, user_pk, template_name='accounts/profil_view.html'):
    u = get_object_or_404(User, pk=user_pk)
    p = None
    try:
        p = u.get_profile()
    except Profil.DoesNotExist:
        p = Profil(user=u)
        p.save()

    return render_to_response(template_name, RequestContext(request, {'profil': p, 'p': p,}))

class Notification:
    def __init__(self, activity, last_known_activity):
        self.activity = activity
        self.is_new = activity.pk > last_known_activity.pk
    
    def to_html(self):
        html = str(self.activity)
        if self.is_new:
            html = "<strong>%s</strong>" % html
        return html

@login_required
def view_notification(request, template_name='accounts/notification_view.html'):
    p = request.user.get_profile()
    notifications = {}
    norefresh = request.GET.get("norefresh")
    activities = LogActivity.objects.exclude(qui=request.user).exclude(type=ContentType.objects.get_for_model(Participant)).order_by("-pk")[:50]
    for a in activities:
        if not notifications.get(a.date.date()):
            notifications[a.date.date()] = []
        notifications[a.date.date()].append(Notification(a, p.last_known_activity))

    notifications = [(k, notifications[k]) for k in sorted(notifications, reverse=True)]
    return render_to_response(template_name, RequestContext(request, {'notifications': notifications,'norefresh': norefresh,}))

@login_required
def markasread_notification(request):
    p = request.user.get_profile()
    p.last_known_activity = LogActivity.getDefault()
    p.save()
    return HttpResponseRedirect(reverse("viewnotification")+"?norefresh=1")
