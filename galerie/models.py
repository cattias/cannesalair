from django.db import models
from django.contrib.auth.models import User
from comment.models import Comment
from django.core.urlresolvers import reverse
import os
from django.template.defaultfilters import slugify

class Galerie(models.Model):
    imgur_id = models.CharField(max_length=255, null=True, blank=True)
    auteur = models.ForeignKey(User, related_name='auteur_galerie_set')
    titre = models.CharField(max_length=255)
    titre_slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    is_created = models.BooleanField(default=False)
    is_intreatment = models.BooleanField(default=False)
    local_path = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    sortie = models.ForeignKey("sortie.Sortie", null=True, blank=True, related_name='sortie_galeries_set')
    comments = models.ManyToManyField(Comment, 
                                         related_name='galerie_comments_set',
                                         null=True, blank=True)
    date_publication = models.DateTimeField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def generate_slug(self):
        slug = slugify(self.titre)
        if Galerie.objects.exclude(pk=self.pk).filter(titre_slug=slug).count() > 0:
            slug = "%s-%s" % (slug, self.pk)
        self.titre_slug = slug
        self.save()

    def __unicode__(self):
        return "%s" % (self.titre)
    
    def get_absolute_url(self):
        return reverse("viewgalerie", kwargs={'slug':self.titre_slug})

    def get_imgur_url(self):
        return "http://imgur.com/a/%s" % self.imgur_id
    
    def get_edit_url(self):
        return reverse("editgalerie", kwargs={'slug':self.titre_slug})

    def get_embeded_url(self):
        return "http://imgur.com/a/%s/embed" % self.imgur_id

class Photo(models.Model):
    hash = models.CharField(max_length=255, null=True, blank=True)
    galerie = models.ForeignKey(Galerie, related_name="photos_set")
    titre = models.CharField(max_length=255, null=True, blank=True)
    titre_slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    is_uploaded = models.BooleanField(default=False)
    is_linked = models.BooleanField(default=False)
    is_intreatment = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    ordre = models.IntegerField(default=0)
    local_path = models.CharField(max_length=255, null=True, blank=True)
    local_url = models.CharField(max_length=255, null=True, blank=True)
    thumb_local_path = models.CharField(max_length=255, null=True, blank=True)
    thumb_local_url = models.CharField(max_length=255, null=True, blank=True)
    filename = models.CharField(max_length=255, null=True, blank=True)
    filesize = models.IntegerField(null=True, blank=True)
    comments = models.ManyToManyField(Comment, 
                                         related_name='photo_comments_set',
                                         null=True, blank=True)
    date_publication = models.DateTimeField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordre']

    def generate_slug(self):
        if not self.titre:
            self.titre = "%s - %s" % (self.galerie.titre, self.filename)
        slug = slugify(self.titre)
        if Photo.objects.exclude(pk=self.pk).filter(titre_slug=slug).count() > 0:
            slug = "%s-%s" % (slug, self.pk)
        self.titre_slug = slug
        self.save()

    def __unicode__(self):
        value = "%s - %s (%s)" % (self.pk, self.hash, self.filename)
        if self.titre:
            value = "%s: %s" % (value, self.titre)
        return value
    
    def get_absolute_url(self):
        return reverse("viewimage", kwargs={'imagehash':self.hash})

    def get_imgur_url(self):
        if self.hash:
            return "http://i.imgur.com/%s.jpg" % self.hash
        else:
            return self.local_url

    def get_imgur_huge_url(self):
        if self.hash:
            return "http://i.imgur.com/%sh.jpg" % self.hash
        else:
            return self.local_url

    def get_imgur_large_url(self):
        return "http://i.imgur.com/%sl.jpg" % self.hash

    def get_imgur_medium_url(self):
        return "http://i.imgur.com/%sm.jpg" % self.hash

    def get_imgur_small_url(self):
        return "http://i.imgur.com/%st.jpg" % self.hash

    def get_imgur_bigsquare_url(self):
        return "http://i.imgur.com/%sb.jpg" % self.hash

    def get_imgur_smallsquare_url(self):
        return "http://i.imgur.com/%ss.jpg" % self.hash

    def get_download_link(self):
        return "http://imgur.com/download/%s" % self.hash
    
    def get_thumbnail_url(self):
        if self.hash:
            return self.get_imgur_smallsquare_url()
        elif self.thumb_local_path and os.path.exists(self.thumb_local_path):
            return self.thumb_local_url

    def get_bigsquare_url(self):
        if self.hash:
            return self.get_imgur_bigsquare_url()
        elif self.thumb_local_path and os.path.exists(self.thumb_local_path):
            return self.thumb_local_url

class DownloadJob(models.Model):
    images = models.ManyToManyField(Photo, 
                                         related_name='photo_downloadjob_set',
                                         null=True, blank=True)
    galerie = models.ForeignKey(Galerie, related_name="galerie_downloadjob_set")
    email = models.EmailField(max_length=255)
    is_intreatment = models.BooleanField(default=False)
    is_treated = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    path_to_zip = models.CharField(max_length=255, null=True, blank=True)
    date_treatment = models.DateTimeField(auto_now=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s for %s (isintreat=%s, isdone=%s, isdeleted=%s)" % (self.galerie.titre_slug, self.email, self.is_intreatment, self.is_treated, self.is_deleted)
