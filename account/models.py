# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from photologue.models import Photo
from django.core.urlresolvers import reverse
from log.models import LogActivity

class Profil(models.Model):
    user = models.ForeignKey(User, default=1)
    lieu = models.TextField(null=True, blank=True)
    telephone = models.TextField(null=True, blank=True)
    avatar = models.ForeignKey(Photo, null=True, blank=True, related_name='avatar_set')
    gravatarurl = models.TextField(null=True, blank=True)
    signature = models.TextField(null=True, blank=True)
    siteweb = models.TextField(null=True, blank=True)
    custom_background_image = models.CharField(max_length=255, null=True, blank=True)
    discussions = models.ManyToManyField("forum.Thread", 
                                         related_name='discussions_suivies_set',
                                         null=True, blank=True)
    forums = models.ManyToManyField("forum.Forum", 
                                         related_name='forums_suivis_set',
                                         null=True, blank=True)
    articles = models.ManyToManyField("article.Article", 
                                         related_name='articles_suivis_set',
                                         null=True, blank=True)
    sorties = models.ManyToManyField("sortie.Sortie", 
                                         related_name='sorties_suivies_set',
                                         null=True, blank=True)
    galeries = models.ManyToManyField("galerie.Galerie", 
                                         related_name='galeries_suivies_set',
                                         null=True, blank=True)
    suivre_les_articles = models.BooleanField(default=True)
    suivre_les_sorties = models.BooleanField(default=True)
    suivre_les_sorties_partype = models.ManyToManyField("sortie.Activite", 
                                         related_name='activites_suivies_set',
                                         null=True, blank=True)
    suivre_les_compterendus = models.BooleanField(default=True)
    suivre_les_discussions = models.BooleanField(default=True)
    suivre_les_galeries = models.BooleanField(default=True)
    auto_refresh_notif = models.BooleanField(default=False)
    last_known_activity = models.ForeignKey(LogActivity, related_name='last_known_activity_set', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s (%s - %s)" % (self.user.username, self.lieu, self.telephone)
    
    def get_avatar_url(self):
        url = "/media/images/default-avatar.png"
        if self.gravatarurl:
            url = self.gravatarurl
        elif self.avatar:
            urltmp = self.avatar.get_avatar_url()
            _file = self.avatar.image.path 
            try:
                import os
                if os.path.isfile(_file):
                    url = urltmp
            except:
                pass
        return url

    def get_avatar_full_url(self):
        url = "/media/images/default-avatar.png"
        if self.gravatarurl:
            url = self.gravatarurl
        elif self.avatar:
            urltmp = self.avatar.image.url
            _file = self.avatar.image.path 
            try:
                import os
                if os.path.isfile(_file):
                    url = urltmp
            except:
                pass
        return url

    def get_html_avatar(self, cssclass="avatar"):
        html = "<a href='%s'><img width='50px' height='50px' class='%s' src='%s' alt='%s'/></a>" % (reverse("viewprofil", kwargs={'user_pk':self.user.pk}), cssclass, self.get_avatar_url(), self.user.username)
        return html

    def get_html_illustration(self):
        return self.get_html_avatar(cssclass="illustration")
