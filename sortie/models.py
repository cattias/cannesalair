# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from comment.models import Comment
from django.core.urlresolvers import reverse
from django.conf import settings
from djangogcal.adapter import CalendarAdapter, CalendarEventData
from djangogcal.observer import CalendarObserver
from django.contrib.sites.models import Site
import datetime
from django.template.defaultfilters import slugify

class Activite(models.Model):
    activite = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % (self.activite)

class SortieType(models.Model):
    name = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=20)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % (self.name)

class CRSortie(models.Model):
    auteur = models.ForeignKey(User, related_name='crsortie_auteur_set')
    compterendu = models.TextField()
    kilometrage = models.IntegerField(null=True, blank=True)
    peages = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    nb_voitures = models.IntegerField(null=True, blank=True)
    participants_effectifs = models.CharField(max_length=255, null=True, blank=True)
    nb_participants_effectifs = models.IntegerField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s, %s" % (self.auteur, self.date_creation)

class Sortie(models.Model):
    auteur = models.ForeignKey(User, related_name='sortie_auteur_set')
    titre = models.TextField()
    titre_slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    lieu = models.TextField()
    rdv = models.TextField(null=True, blank=True)
    typesortie = models.ForeignKey(SortieType, verbose_name='Type', related_name='sortie_type_set', default=1)
    description = models.TextField()
    cr = models.ForeignKey(CRSortie, related_name='compte_rendu_sortie_set', null=True, blank=True)
    date_debut = models.DateTimeField(verbose_name='Date de début')
    date_fin = models.DateTimeField(verbose_name='Date de fin')
    comments = models.ManyToManyField(Comment, 
                                         related_name='sortie_comments_set',
                                         null=True, blank=True)
    activites = models.ManyToManyField(Activite, verbose_name='Catégories',
                                          related_name='activites_sortie_set',
                                          null=True, blank=True)
    canceled = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    def get_type_label(self):
        return self.typesortie.name

    def __unicode__(self):
        date = "%s" % self.date_debut.date().strftime("%d/%m/%Y")
        if not self.date_debut.date() == self.date_fin.date():
            date = "%s - %s" % (date, self.date_fin.date().strftime("%d/%m/%Y"))
        return "[%s] %s (%s)" % (date, self.titre, self.lieu)

    def get_short_date_string(self):
        datestr = "%s" % self.date_debut.strftime("%d/%m")
        if not (self.date_debut.day == self.date_fin.day and self.date_debut.month == self.date_fin.month and self.date_debut.year == self.date_fin.year):
            datestr += "-%s" % self.date_fin.strftime("%d/%m")
        return datestr

    def generate_slug(self):
        slug = slugify(self.titre)
        oldslug = self.titre_slug
        if oldslug:
            try:
                SortieOldSlugs.objects.get_or_create(sortie=self, titre_slug=oldslug)
            except:
                pass
        if Sortie.objects.exclude(pk=self.pk).filter(titre_slug=slug).count() + SortieOldSlugs.objects.exclude(sortie=self).filter(titre_slug=slug).count() > 0:
            slug = "%s-%s" % (slug, self.pk)
        self.titre_slug = slug
        self.save()

    def get_absolute_url(self):
        return reverse("viewsortie", kwargs={'slug':self.titre_slug})
    
    class Meta:
        ordering = ['-date_debut']

class Participant(models.Model):
    STATUT = (
        ('oui', 'Oui'),
        ('non', 'Non'),
        ('peutetre', u'Peut-\u00eatre'),
    )
    qui = models.ForeignKey(User, related_name='participant_user_set')
    sortie = models.ForeignKey(Sortie, related_name='participant_sortie_set')
    statut = models.CharField(max_length=20, choices=STATUT)
    date_update = models.DateTimeField()

    def __unicode__(self):
        return u"%s" % (self.qui.username)

class SpecialParticipant(models.Model):
    STATUT = (
        ('oui', 'Oui'),
        ('peutetre', u'Peut-\u00eatre'),
    )
    qui = models.ForeignKey(User, related_name='participant_garant_user_set')
    nom = models.CharField(max_length=255)
    email = models.EmailField()
    sortie = models.ForeignKey(Sortie, related_name='participant_special_sortie_set')
    statut = models.CharField(max_length=20, choices=STATUT)
    date_update = models.DateTimeField()

    def __unicode__(self):
        return u"%s" % (self.qui.username)

class SortieOldSlugs(models.Model):
    sortie = models.ForeignKey(Sortie, related_name='sortie_oldslugs_set')
    titre_slug = models.SlugField(max_length=255, unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % (self.titre_slug)
    
class SortieCalendarAdapter(CalendarAdapter):
    """
    A calendar adapter for the Sortie model.
    """
    
    def get_event_data(self, instance):
        """
        Returns a CalendarEventData object filled with data from the adaptee.
        """
        try:
            description = "<a href='http://%s%s'>Voir le d&eacute;tail de l'activit&eacute;</a><br/>%s" % (Site.objects.get(pk=settings.SITE_ID).domain, instance.get_absolute_url(), instance.description)
            titre = "%s: %s" % (instance.get_type_label(), instance.titre)
            start = instance.date_debut
            end = instance.date_fin
            if end.time() == datetime.time(0, 0):
                end = end + datetime.timedelta(days=1)
            return CalendarEventData(
                start=start,
                end=end,
                title=titre,
                where=[instance.lieu, "RDV: %s" % instance.rdv,],
                content=description,
            )
        except:
            return None

observer = CalendarObserver(email=settings.CALENDAR_EMAIL,
                            password=settings.CALENDAR_PASSWORD)
observer.observe(Sortie, SortieCalendarAdapter())
