# -*- coding: utf-8 -*-
from sortie.models import Sortie, Participant, SortieOldSlugs,\
    SpecialParticipant
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q
import datetime
from django.contrib.auth.models import User, Group
from django.http import Http404, HttpResponseRedirect
from django import forms
from log.models import LogActivity
from core.widgets import MediumTextInput
from sortie.context_processors import sortiesavenir

def calendar_sorties(request, template_name='sortie/sortie_calendar.html'):
    return render_to_response(template_name, RequestContext(request,{'full': True}))

def list_sorties(request, template_name='sortie/sortie_list.html'):
    now = datetime.datetime.now()
    now = now - datetime.timedelta(days=1)
    sortiesavenirfiltered = Sortie.objects.filter(date_fin__gte=now).order_by('date_debut')
    sortiespassees = Sortie.objects.filter(date_fin__lt=now).order_by('-date_debut')

    years = []
    for s in sortiespassees:
        if not s.date_fin.year in years:
            years.append(s.date_fin.year)
        if not s.date_debut.year in years:
            years.append(s.date_debut.year)
    for s in sortiesavenirfiltered:
        if not s.date_fin.year in years:
            years.append(s.date_fin.year)
        if not s.date_debut.year in years:
            years.append(s.date_debut.year)
    year = request.GET.get("year", None)

    tags = request.GET.getlist('cat')
    if tags:
        query_or = Q()
        for t in tags:
            query_or |= Q(activites__activite__icontains=t)
        sortiesavenirfiltered = sortiesavenirfiltered.filter(query_or)
        sortiespassees = sortiespassees.filter(query_or)
    
    auteur = request.GET.get('auteur')
    if auteur:
        auteur = User.objects.get(pk=int(auteur))
        sortiesavenirfiltered = sortiesavenirfiltered.filter(auteur=auteur)
        sortiespassees = sortiespassees.filter(auteur=auteur)

    view = request.GET.get('view')
    if not view == 'all' and not tags and not auteur:
        if not year:
            year = datetime.date.today().year
        else:
            year = int(year)
        query = Q(date_fin__year=year) | Q(date_debut__year=year)
        sortiespassees = sortiespassees.filter(query)
        query = Q(date_fin__year=year) | Q(date_debut__year=year) | Q(date_fin__year=year+1) | Q(date_debut__year=year+1)
        sortiesavenirfiltered = sortiesavenirfiltered.filter(query)

    sortiesavenirfilteredcount = sortiesavenirfiltered.count()
    sortiespasseescount = sortiespassees.count()
    return render_to_response(template_name,
                              RequestContext(request,
                                             {'auteur': auteur,
                                              'sortiesavenirfiltered': sortiesavenirfiltered,
                                              'sortiesavenirfilteredcount': sortiesavenirfilteredcount,
                                              'sortiespassees': sortiespassees,
                                              'sortiespasseescount': sortiespasseescount,
                                              'years': years,
                                              'year': year,
                                              'cats': tags,
                                              'view': view,
                                              }))

def view_sortie(request, slug, template_name='sortie/sortie_view.html'):
    try:
        sortie = Sortie.objects.get(titre_slug=slug)
    except Sortie.DoesNotExist:
        try:
            sortie = Sortie.objects.get(pk=int(slug))
        except:
            try:
                old = SortieOldSlugs.objects.get(titre_slug=slug)
                if old:
                    sortie = old.sortie
                else:
                    raise Http404("L'activit&eacute; n'existe pas")
            except SortieOldSlugs.DoesNotExist:
                raise Http404("L'activit&eacute; n'existe pas")
    return internal_view_sortie(request, sortie, template_name=template_name)

class SpecialParticipantForm(forms.ModelForm):
    nom = forms.CharField(required=True, widget=MediumTextInput)
    email = forms.EmailField(required=True, widget=MediumTextInput)

    class Meta:
        model = SpecialParticipant
        fields = ['nom', 'email']

def internal_view_sortie(request, sortie, crsortie=None, template_name='sortie/sortie_view.html', urlretour=None, categories=None):
    date_publication = sortie.date_creation if sortie.date_creation else datetime.datetime.now()
    canbeedited = not urlretour and (request.user == sortie.auteur or request.user.is_superuser)
    if not crsortie:
        crsortie = sortie.cr
    
    caneditcr = canbeedited or (not urlretour and ((crsortie and request.user == crsortie.auteur) or request.user.is_superuser or request.user in [p.qui for p in sortie.participant_sortie_set.filter(statut='oui')]))
    canviewspecificcr = crsortie and request.user.is_authenticated() and (Group.objects.filter(user=request.user, name="Bureau").count() > 0 or request.user.is_superuser or crsortie.auteur == request.user)
    poui = sortie.participant_sortie_set.filter(statut='oui') if sortie.pk else []
    pnon = sortie.participant_sortie_set.filter(statut='non') if sortie.pk else []
    ppe = sortie.participant_sortie_set.filter(statut='peutetre') if sortie.pk else []

    spoui = sortie.participant_special_sortie_set.filter(statut='oui') if sortie.pk else []
    sppe = sortie.participant_special_sortie_set.filter(statut='peutetre') if sortie.pk else []

    totalpe = ppe.count() + sppe.count()
    totalsur = poui.count() + spoui.count()
    totalfull = totalpe + totalsur

    issubscribed = False
    if request.user.is_authenticated() and sortie.pk:
        issubscribed = request.user.get_profile() in sortie.sorties_suivies_set.all()
    
    maparticipation = None
    mesinvites = None
    if request.user.is_authenticated() and sortie.pk:
        maparticipation = Participant.objects.filter(qui=request.user, sortie=sortie)
        mesinvites = SpecialParticipant.objects.filter(sortie=sortie, qui=request.user)
        if maparticipation.count() > 0:
            maparticipation = maparticipation[0]
        else:
            maparticipation = None

    spform = SpecialParticipantForm()
    
    if request.method == 'POST': # If the form has been submitted...
        spform = SpecialParticipantForm(request.POST)
        if spform.is_valid():
            special_participant = spform.save(commit=False)
            special_participant.qui = request.user
            special_participant.sortie = sortie
            special_participant.statut = request.POST.get('statut')
            special_participant.date_update = datetime.datetime.now()
            special_participant.save()
            LogActivity.recordActivity(qui=request.user, quoi=sortie, comment="a ajout&eacute; un(e) participant(e) sp&eacute;cial(e) &agrave; l'activit&eacute; <a href='%s'>%s</a>" % (sortie.get_absolute_url(), sortie.titre))
            # Redirect after POST
            return HttpResponseRedirect(sortie.get_absolute_url())
    
    return render_to_response(template_name, RequestContext(request, 
                                                            {'sortie': sortie,
                                                             'date_publication': date_publication,
                                                             'urlretour': urlretour,
                                                             'canbeedited': canbeedited,
                                                             'crsortie': crsortie,
                                                             'caneditcr': caneditcr,
                                                             'canviewspecificcr': canviewspecificcr,
                                                             'mesinvites': mesinvites,
                                                             'spform': spform,
                                                             'full': True,
                                                             'poui': poui,
                                                             'pouicount': poui.count(),
                                                             'pnon': pnon,
                                                             'pnoncount': pnon.count(),
                                                             'ppe': ppe,
                                                             'ppecount': ppe.count(),
                                                             'spoui': spoui,
                                                             'spouicount': spoui.count(),
                                                             'sppe': sppe,
                                                             'sppecount': sppe.count(),
                                                             'totalfull': totalfull,
                                                             'totalpe': totalpe,
                                                             'totalsur': totalsur,
                                                             'maparticipation': maparticipation,
                                                             'issubscribed': issubscribed,
                                                             'categories': categories,
                                                             }))
