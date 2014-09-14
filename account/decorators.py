'''
Created on Nov 12, 2009

@author: cattias
'''
from django.http import HttpResponseRedirect
from djblets.util.decorators import simple_decorator
import urllib
from django.core.urlresolvers import reverse


@simple_decorator
def profil_required(view_func):
    """
    Profil is required to access some pages
    """
    def _checkprofil(request, *args, **kwargs):
        if request.user.is_anonymous():
            return view_func(request, *args, **kwargs)
        else:
            p = request.user.get_profile()
            if p:
                return view_func(request, *args, **kwargs)
            else:
                next = "%s?next_page=%s" % (reverse("editprofil"), request.path)
                if request.META and request.META['QUERY_STRING']:
                    next += "&next_query=%s" % urllib.quote_plus(request.META['QUERY_STRING'])
                return HttpResponseRedirect(next)
    return _checkprofil

@simple_decorator
def login_required(view_func):
    """
    New version of auth.decorators.login_required,
    which adds a 'next_query' parameter used in addition to the 'next_page' one.
    """
    def _checklogin(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        else:
            next = "%s?next_page=%s" % (reverse("login"), request.path)
            if request.META and request.META['QUERY_STRING']:
                next += "&next_query=%s" % urllib.quote_plus(request.META['QUERY_STRING'])
            return HttpResponseRedirect(next)
    return _checklogin
