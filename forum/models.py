# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

class Groupe(models.Model):
    titre = models.TextField()
    titre_slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    ordre = models.IntegerField()
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return "%s" % (self.titre)

class Forum(models.Model):
    titre = models.TextField()
    titre_slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    groupe = models.ForeignKey(Groupe, related_name='groupe_forum_set')
    commentaire = models.TextField()
    moderateurs = models.ManyToManyField(User, 
                                         related_name='forum_moderateur_set',
                                         null=True, blank=True)
    ordre = models.IntegerField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("showforum", kwargs={'slug':self.titre_slug})
        
    def __unicode__(self):
        return "%s" % (self.titre)

class Thread(models.Model):
    titre = models.TextField()
    titre_slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    forum = models.ForeignKey(Forum, related_name='forum_thread_set')
    date_creation = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("showthread", kwargs={'slug':self.titre_slug})
    
    def generate_slug(self):
        slug = slugify(self.titre)
        if Thread.objects.exclude(pk=self.pk).filter(titre_slug=slug).count() > 0:
            slug = "%s-%s" % (slug, self.pk)
        self.titre_slug = slug
        self.save()
    
    def __unicode__(self):
        return "%s" % (self.titre)

class Message(models.Model):
    auteur = models.ForeignKey(User, related_name='auteur_message_set')
    contenu = models.TextField()
    thread = models.ForeignKey(Thread, related_name='thread_message_set')
    date_publication = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s - %s - %s" % (self.pk, self.auteur.username, self.date_publication)

