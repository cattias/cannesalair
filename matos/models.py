# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from photologue.models import Gallery

class Categorie(models.Model):
    name = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % (self.name)
    
class SousCategorie(models.Model):
    name = models.TextField()
    categorie = models.ForeignKey(Categorie, related_name='sous_cat_set')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s : %s" % (self.categorie.name, self.name)

class Matos(models.Model):
    titre = models.TextField()
    description = models.TextField()
    categorie = models.ForeignKey(SousCategorie, related_name='sous_cat_matos_set',
                                        null=True, blank=True)
    prix_neuf = models.FloatField()
    date_achat = models.DateField()
    photos = models.ForeignKey(Gallery, related_name='matos_photos_set', 
                               null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % (self.titre)

    def get_absolute_url(self):
        return reverse("viewmatos", kwargs={'matos_pk':self.pk})        


class Emprunt(models.Model):
    STATUT = (
        ('V', 'En cours'),
        ('R', 'Rendu'),
    )
    qui = models.ForeignKey(User, related_name='emprunteur_set')
    quoi = models.ForeignKey(Matos, related_name='matos_emprunt_set')
    lieu = models.TextField()
    statut = models.CharField(max_length=1, default='V', choices=STATUT)
    date_debut = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % (self.quoi)

