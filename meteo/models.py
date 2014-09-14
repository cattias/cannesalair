# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from comment.models import Comment
import datetime
from sortie.models import Activite

class Prevision(models.Model):
    class Meta:
        ordering = ('date_previ',)
        unique_together = (("auteur", "date_previ"))

    auteur = models.ForeignKey(User, related_name='previ_auteur_set')
    description = models.TextField()
    sources = models.TextField(null=True, blank=True)
    annexe = models.TextField(null=True, blank=True)
    date_previ = models.DateField()
    date_creation = models.DateTimeField(auto_now=True)
    comments = models.ManyToManyField(Comment, 
                                         related_name='previ_comments_set',
                                         null=True, blank=True)

    def __unicode__(self):
        return "Prevision de %s pour le %s" % (self.auteur, self.date_previ)

    def get_titre(self):
        return u"Prévision de %s" % (self.auteur)

    def get_full_titre(self):
        return u"Prévision de %s pour le %s" % (self.auteur, self.date_previ.strftime("%A %d %B %Y"))

    def get_absolute_url(self):
        return reverse("viewprevi", kwargs={"previid": self.pk})

    def get_next_previ(self):
        nextprevi = None
        previ = Prevision.objects.filter(date_previ__gt=self.date_previ)
        if previ:
            nextprevi = Prevision.objects.filter(date_previ=previ[0].date_previ)
        return nextprevi

    def get_next_previ_date(self):
        nextprevidate = None
        previ = Prevision.objects.filter(date_previ__gt=self.date_previ)
        if previ:
            nextprevidate = previ[0].date_previ
        return nextprevidate

    def get_previous_previ(self):
        previousprevi = None
        previ = Prevision.objects.filter(date_previ__gte=datetime.datetime.now(), date_previ__lt=self.date_previ).order_by('-date_previ')
        if previ:
            previousprevi = Prevision.objects.filter(date_previ=previ[0].date_previ)
        return previousprevi

    def get_previous_previ_date(self):
        previousprevidate = None
        previ = Prevision.objects.filter(date_previ__gte=datetime.datetime.now(), date_previ__lt=self.date_previ).order_by('-date_previ')
        if previ:
            previousprevidate = previ[0].date_previ
        return previousprevidate

    @staticmethod
    def get_next_previ_from_date(date):
        nextprevi = None
        previ = Prevision.objects.filter(date_previ__gte=date)
        if previ:
            nextprevi = Prevision.objects.filter(date_previ=previ[0].date_previ)
        return nextprevi

class Note(models.Model):
    note = models.IntegerField(default=0)
    prevision = models.ForeignKey(Prevision, related_name="prevision_notes_set")
    activite = models.ForeignKey(Activite, related_name="activite_notes_set")
    date_creation = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s : %s/4" % (self.activite.activite, self.note)
    
    class Meta:
        ordering = ('activite',)
        unique_together = (("prevision", "activite"))

