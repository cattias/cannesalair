from django.shortcuts import render_to_response, get_object_or_404
from meteo.models import Prevision, Note
from django.template.context import RequestContext
import datetime
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django import forms
from core.widgets import MediumTextInput
from django.forms.util import ErrorList

def list_previ(request, template_name='meteo/previ_list.html'):
    now = datetime.datetime.now()
    now = now - datetime.timedelta(days=1)
    previavenir = Prevision.objects.filter(date_previ__gte=now).order_by('-date_previ')
    previpassees = Prevision.objects.filter(date_previ__lt=now).order_by('-date_previ')

    years = []
    for s in previpassees:
        if not s.date_previ.year in years:
            years.append(s.date_previ.year)
    year = request.GET.get("year", None)

    auteur = request.GET.get('auteur')
    if auteur:
        auteur = User.objects.get(pk=int(auteur))
        previavenir = previavenir.filter(auteur=auteur)
        previpassees = previpassees.filter(auteur=auteur)

    view = request.GET.get('view')
    if not view == 'all' and not auteur:
        if not year:
            year = datetime.date.today().year
        else:
            year = int(year)
        query = Q(date_previ__year=year)
        previpassees = previpassees.filter(query)

    previavenircount = previavenir.count()
    previpasseescount = previpassees.count()
    return render_to_response(template_name,
                              RequestContext(request,
                                             {'auteur': auteur,
                                              'previavenir': previavenir,
                                              'previavenircount': previavenircount,
                                              'previpassees': previpassees,
                                              'previpasseescount': previpasseescount,
                                              'years': years,
                                              'year': year,
                                              'view': view,
                                              }))

class NoteForm(forms.ModelForm):
    prevision = forms.ModelChoiceField(queryset=Prevision.objects.all(), widget=forms.HiddenInput)
    note = forms.IntegerField(required=True, label='Note sur 4', widget=MediumTextInput)

    class Meta:
        model = Note
        fields = ['prevision', 'activite', 'note']

    def __init__(self, previ, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):
        if not initial:
            initial = {'prevision': previ.pk}
        else:
            initial['prevision'] = previ.pk
        super(NoteForm, self).__init__(data=data, files=files, auto_id=auto_id, prefix=prefix,
                 initial=initial, error_class=error_class, label_suffix=label_suffix,
                 empty_permitted=empty_permitted, instance=instance)

def view_previ(request, previid, template_name='meteo/previ_view.html'):
    previ = get_object_or_404(Prevision, pk=previid)
    return internal_view_previ(request, previ, template_name=template_name)

def internal_view_previ(request, previ, template_name='meteo/previ_view.html', urlretour=None):
    canbeedited = not urlretour and (request.user == previ.auteur or request.user.is_superuser)

    if request.GET.get("action") == "delete":
        note = get_object_or_404(Note, pk=int(request.GET.get("pk")))
        note.delete()
        previ.save()
        return HttpResponseRedirect(previ.get_absolute_url())

    noteform = NoteForm(previ=previ)
    if request.method == 'POST': # If the form has been submitted...
        noteform = NoteForm(previ=previ, data=request.POST)
        if noteform.is_valid():
            note = noteform.save(commit=False)
            note.save()
            previ.save()
            # Redirect after POST
            return HttpResponseRedirect(previ.get_absolute_url())

    return render_to_response(template_name, RequestContext(request, 
                                                            {'previ': previ,
                                                             'urlretour': urlretour,
                                                             'canbeedited': canbeedited,
                                                             'noteform': noteform,
                                                             'full': True,
                                                             }))

def encartmeteo(request, template_name='meteo/encart_meteo.html'):
    date = request.GET.get('date', None)
    if not date:
        date = datetime.datetime.now()
    else:
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
    previsions = Prevision.get_next_previ_from_date(date)
    nexturl = None
    previousurl = None
    if previsions:
        next_previ_date = previsions[0].get_next_previ_date()
        previous_previ_date = previsions[0].get_previous_previ_date()
        if next_previ_date:
            nexturl = "%s?date=%s" % (reverse("encartmeteo"), next_previ_date.strftime("%Y-%m-%d"))
        if previous_previ_date:
            previousurl = "%s?date=%s" % (reverse("encartmeteo"), previous_previ_date.strftime("%Y-%m-%d"))
        
    return render_to_response(template_name, RequestContext(request, {"previsions": previsions,
                                                                      "nexturl": nexturl,
                                                                      "previousurl": previousurl,
                                                                      }))
    