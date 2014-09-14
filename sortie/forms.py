# -*- coding: utf-8 -*-
"""
Forms for sortie
"""
from django import forms
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.contrib.auth.models import User
from core.widgets import TextareaTiny, MediumTextInput, CustomDatePicker
from sortie.models import Sortie, Participant, Activite, CRSortie,\
    SpecialParticipant
from account.decorators import login_required
from core.mail import internal_sendmail, add_to_maillist
from django.contrib.sites.models import Site
from log.models import LogActivity
import datetime
from sortie.views import internal_view_sortie
from account.models import Profil
from account.decorators import profil_required
import threading

class SortieForm(forms.ModelForm):
    auteur = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
    titre = forms.CharField(required=True, label='Titre', widget=MediumTextInput)
    lieu = forms.CharField(required=True, label='Lieu', widget=MediumTextInput)
    date_debut = forms.DateTimeField(required=True, label=u'Date de début', widget=CustomDatePicker(attrs={'id':'datepicker_date_debut', 'name': 'date_debut'}))
    date_fin = forms.DateTimeField(required=True, label=u'Date de fin', widget=CustomDatePicker(attrs={'id':'datepicker_date_fin', 'name': 'date_fin'}))
    rdv = forms.CharField(required=False, label='Lieu de RDV', widget=MediumTextInput)
    description = forms.CharField(required=True, label='Description', widget=TextareaTiny(attrs={'rows':'30', 'cols':'100'}))
    activites = forms.ModelMultipleChoiceField(queryset=Activite.objects.all(), required=True, label=u'Catégories', help_text=None)

    class Meta:
        model = Sortie
        fields = ['auteur', 'titre', 'lieu', 'rdv', 'typesortie', 'description', 'date_debut', 'date_fin', 'activites']


class CompteRenduSortieForm(forms.ModelForm):
    compterendu = forms.CharField(required=True, label='Compte-rendu', widget=TextareaTiny(attrs={'rows':'30', 'cols':'100'}))
    kilometrage = forms.IntegerField(required=False, label='Kilométrage', widget=MediumTextInput)
    peages = forms.DecimalField(required=False, label='Péages', widget=MediumTextInput)
    nb_voitures = forms.IntegerField(required=False, label='Nombre de voitures', widget=MediumTextInput)
    participants_effectifs = forms.CharField(required=False, label='Liste des participants effectifs', widget=MediumTextInput)
    nb_participants_effectifs = forms.IntegerField(required=False, label='Nombre de participants effectifs', widget=MediumTextInput)
    notification = forms.BooleanField(required=False, label=u'Ne pas envoyer de notification')

    class Meta:
        model = CRSortie
        fields = ['compterendu', 'kilometrage', 'peages', 'nb_voitures', 'participants_effectifs', 'nb_participants_effectifs']

@login_required
def cancel_sortie(request, slug):
    sortie = Sortie.objects.get(titre_slug=slug)
    sortie.canceled = True
    sortie.save()
    return HttpResponseRedirect(sortie.get_absolute_url())

@login_required
def uncancel_sortie(request, slug):
    sortie = Sortie.objects.get(titre_slug=slug)
    sortie.canceled = False
    sortie.save()
    return HttpResponseRedirect(sortie.get_absolute_url())

@login_required
def edit_sortie_cr(request, slug, template_name='sortie/sortie_edit_cr.html'):
    sortie = Sortie.objects.get(titre_slug=slug)
    first_time = sortie.cr is None

    if request.method == 'POST': # If the form has been submitted...
        preview = request.POST.get('preview', None)
        editpreview = request.POST.get('editpreview', None)
        if first_time:
            new_form = CompteRenduSortieForm(request.POST)
        else:
            new_form = CompteRenduSortieForm(request.POST, instance=sortie.cr)
        if not editpreview and new_form.is_valid():
            new_crsortie = new_form.save(commit=False)
            if first_time:
                new_crsortie.auteur = request.user
            if not preview:
                new_crsortie.save()
                sortie.cr = new_crsortie
                sortie.save()
                if first_time and not request.POST.get('notification'):
                    ThreadCompteRenduMail(sortie, request.user).start()
                LogActivity.recordActivity(qui=request.user, quoi=sortie, comment="a modifi&eacute; le compte-rendu de l'activit&eacute; <a href='%s'>%s</a>" % (sortie.get_absolute_url(), sortie.titre))
                # Redirect after POST
                return HttpResponseRedirect(sortie.get_absolute_url())
            else:
                cat = sortie.activites.all()
                return internal_view_sortie(request, sortie, crsortie=new_crsortie, urlretour=reverse("editsortiecr", kwargs={"slug":slug}), categories=cat)
        else:
            form = new_form
    else:
        if first_time:
            form = CompteRenduSortieForm()
        else:
            form = CompteRenduSortieForm(instance=sortie.cr)
    return render_to_response(template_name,
                              RequestContext(request,
                                             {'form': form,
                                              'sortie': sortie,
                                              'full': True,
                                              }))

def send_notification_compterendu(sortie, auteur, template_name="sortie/compterendu_mail.html"):
    current_site = Site.objects.get_current()
    site_name = current_site.name
    domain = current_site.domain
    maillist = []
        
    for p in sortie.sorties_suivies_set.all():
        add_to_maillist(maillist, p.user, auteur)

    for p in Profil.objects.filter(suivre_les_compterendus=True):
        add_to_maillist(maillist, p.user, auteur)

    subject = "[CAL - Compte-Rendu](%s) %s" % (sortie.get_short_date_string(), sortie.titre)
    from_email = "Les Cannes A L'air <no-reply@cannesalair.fr>"
    for u in maillist:
        text = render_to_string(template_name, {'site_name': site_name,
                                                'domain': domain,
                                                'user': auteur,
                                                'sortie': sortie,
                                                'profil': u,
                                                })
        internal_sendmail(u.email, from_email, text, subject)

class ThreadCompteRenduMail(threading.Thread):
    def __init__(self, sortie, auteur):
        threading.Thread.__init__(self)
        self.sortie = sortie
        self.auteur = auteur
        
    def run(self):
        send_notification_compterendu(self.sortie, self.auteur)

@login_required
def add_sortie(request, template_name='sortie/sortie_add.html'):
    if request.method == 'POST': # If the form has been submitted...
        preview = request.POST.get('preview', None)
        editpreview = request.POST.get('editpreview', None)
        new_form = SortieForm(request.POST)
        if not editpreview and new_form.is_valid():
            new_sortie = new_form.save(commit=False)
            if not preview:
                new_sortie.save()
                new_sortie.generate_slug()
                new_sortie.activites.clear()
                for a in request.POST.getlist("activites"):
                    new_sortie.activites.add(a)
                LogActivity.recordActivity(qui=request.user, quoi=new_sortie, comment="a ajout&eacute; l'activit&eacute; <a href='%s'>%s</a>" % (new_sortie.get_absolute_url(), new_sortie.titre))
                subscribe_sortie(new_sortie.auteur.get_profile(), new_sortie)
                ThreadMail(new_sortie).start()
                # Redirect after POST
                return HttpResponseRedirect(new_sortie.get_absolute_url())
            else:
                cat = Activite.objects.filter(pk__in=request.POST.getlist("activites"))
                return internal_view_sortie(request, new_sortie, urlretour=reverse("addsortie"), categories=cat)
        else:
            form = new_form
    else:
        init = {}
        init['auteur'] = request.user.pk
        form = SortieForm(initial=init)
    return render_to_response(template_name,
                              RequestContext(request,
                                             {'form': form,
                                              'full': True,
                                              }))

def send_notification_new_sortie(sortie, template_name="sortie/mail_new_sortie.html"):
    current_site = Site.objects.get_current()
    site_name = current_site.name
    domain = current_site.domain
    maillist = []
        
    for p in Profil.objects.filter(suivre_les_sorties=True):
        add_to_maillist(maillist, p.user, sortie.auteur)
    for p in Profil.objects.filter(suivre_les_sorties_partype__in=sortie.activites.all()):
        add_to_maillist(maillist, p.user, sortie.auteur)

    subject = "[CAL](%s) %s" % (sortie.get_short_date_string(), sortie.titre)
    from_email = "Les Cannes A L'air <no-reply@cannesalair.fr>"
    for u in maillist:
        text = render_to_string(template_name, {'site_name': site_name,
                                                'domain': domain,
                                                'user': sortie.auteur,
                                                'sortie': sortie,
                                                'profil': u,
                                                })
        internal_sendmail(u.email, from_email, text, subject)

class ThreadMail(threading.Thread):
    def __init__(self, sortie):
        threading.Thread.__init__(self)
        self.sortie = sortie
        
    def run(self):
        send_notification_new_sortie(self.sortie)

@login_required
def edit_sortie(request, slug, template_name='sortie/sortie_edit.html'):
    sortie = Sortie.objects.get(titre_slug=slug)
    if request.method == 'POST': # If the form has been submitted...
        preview = request.POST.get('preview', None)
        editpreview = request.POST.get('editpreview', None)
        new_form = SortieForm(request.POST, instance=sortie)
        if not editpreview and new_form.is_valid():
            new_sortie = new_form.save(commit=False)
            if not preview:
                new_sortie.save()
                new_sortie.generate_slug()
                new_sortie.activites.clear()
                for a in request.POST.getlist("activites"):
                    new_sortie.activites.add(a)
                LogActivity.recordActivity(qui=request.user, quoi=new_sortie, comment="a modifi&eacute; l'activit&eacute; <a href='%s'>%s</a>" % (sortie.get_absolute_url(), sortie.titre))
                # Redirect after POST
                return HttpResponseRedirect(sortie.get_absolute_url())
            else:
                cat = Activite.objects.filter(pk__in=request.POST.getlist("activites"))
                return internal_view_sortie(request, new_sortie, urlretour=reverse("editsortie", kwargs={"slug": slug}), categories=cat)
        else:
            form = new_form
    else:
        form = SortieForm(instance=sortie)
    return render_to_response(template_name,
                              RequestContext(request,
                                             {'form': form,
                                              'sortie': sortie,
                                              'full': True,
                                              }))

@login_required
def participer_sortie(request, slug):
    return _manage_participation(request, slug, "oui")

@login_required
def participerpeutetre_sortie(request, slug):
    return _manage_participation(request, slug, "peutetre")

@login_required
def annulerparticiper_sortie(request, slug):
    return _manage_participation(request, slug, "non")

def _manage_participation(request, slug, statut):
    qui = request.user
    sortie = Sortie.objects.get(titre_slug=slug)
    pp = Participant.objects.filter(qui=qui, sortie=sortie)
    participant = None
    if pp and pp.count() > 0:
        participant = pp[0]

    if not participant:
        participant = Participant(qui=qui, sortie=sortie)
    
    if not participant.statut == statut: 
        participant.statut = statut
        participant.date_update = datetime.datetime.now()
        participant.save()
        subscribe_sortie(qui.get_profile(), sortie)
        LogActivity.recordActivity(qui=qui, quoi=participant, comment="a modifi&eacute; sa participation &agrave; l'activit&eacute; <a href='%s'>%s</a> : %s" % (sortie.get_absolute_url(), sortie.titre, dict(Participant.STATUT)[statut]), surquoi=sortie)
        ThreadParticipationMail(sortie, qui, statut).start()

    return HttpResponseRedirect(sortie.get_absolute_url())
    
def send_participation_mail(sortie, nouveau, statut, template_name="sortie/participation_mail.html"): 
    current_site = Site.objects.get_current()
    site_name = current_site.name
    domain = current_site.domain
    maillist = []

    # Seulement l'auteur est notifie des changements de participation
    add_to_maillist(maillist, sortie.auteur, nouveau)

    participationstr = "What the Fuck !!"
    if statut == "oui":
        participationstr = u"participe"
    elif statut == "non":
        participationstr = u"ne participe pas"
    elif statut == "peutetre":
        participationstr = u"participe potentiellement"
    subject = u"[CAL](%s) Je %s à '%s'" % (sortie.get_short_date_string(), participationstr, sortie.titre)
    from_email = "Les Cannes A L'air <no-reply@cannesalair.fr>"
    for u in maillist:
        text = render_to_string(template_name, {'site_name': site_name,
                                                'domain': domain,
                                                'user': nouveau,
                                                'profil':u,
                                                'sortie': sortie,
                                                })
        internal_sendmail(u.email, from_email, text, subject)

class ThreadParticipationMail(threading.Thread):
    def __init__(self, sortie, nouveau, statut):
        threading.Thread.__init__(self)
        self.sortie = sortie
        self.nouveau = nouveau
        self.statut = statut
        
    def run(self):
        send_participation_mail(self.sortie, self.nouveau, self.statut)

@login_required
def delete_sortie(request, slug):
    sortie = Sortie.objects.get(titre_slug=slug)
    if sortie:
        sortie.delete()
    return HttpResponseRedirect(reverse("sorties"))

@login_required
@profil_required
def subscribe_sortie_slug(request, slug):
    s = Sortie.objects.get(titre_slug=slug)
    subscribe_sortie(request.user.get_profile(), s)
    return HttpResponseRedirect(s.get_absolute_url())

def subscribe_sortie(profile, sortie):
    if profile and sortie not in profile.sorties.all():
        profile.sorties.add(sortie)

@login_required
@profil_required
def unsubscribe_sortie_slug(request, slug):
    s = Sortie.objects.get(titre_slug=slug)
    unsubscribe_sortie(request.user.get_profile(), s)
    next_page = request.GET.get('next_page')
    if next_page:
        return HttpResponseRedirect(next_page)
    else:
        return HttpResponseRedirect(s.get_absolute_url())

def unsubscribe_sortie(profile, sortie):
    if profile and sortie in profile.sorties.all():
        profile.sorties.remove(sortie)

@login_required
def change_specialparticipant(request, spid):
    sp = get_object_or_404(SpecialParticipant, id=spid)
    sortie = sp.sortie
    statut = request.GET.get('statut')
    if request.user == sp.qui:
        if statut == "non":
            sp.delete()
        else:
            sp.statut = statut
            sp.date_update = datetime.datetime.now()
            sp.save()
    return HttpResponseRedirect(sortie.get_absolute_url())


