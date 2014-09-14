# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from tagging.fields import TagField
from comment.models import Comment
from django.core.urlresolvers import reverse
from tagging.utils import parse_tag_input
from django.template.defaultfilters import slugify

tagfield_help_text = 'Separate tags with spaces, put quotes around multiple-word tags.'

class Article(models.Model):
    auteur = models.ForeignKey(User, related_name='auteur_set')
    titre = models.TextField()
    titre_slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    contenu = models.TextField()
    tags = TagField(help_text=tagfield_help_text, verbose_name='tags')
    comments = models.ManyToManyField(Comment, 
                                         related_name='article_comments_set',
                                         null=True, blank=True)
    date_publication = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s (%s - %s)" % (self.titre, self.auteur.username, self.date_publication)
    
    def get_absolute_url(self):
        return reverse("viewarticle", kwargs={'slug':self.titre_slug})
    
    def generate_slug(self):
        slug = slugify(self.titre)
        oldslug = self.titre_slug
        if oldslug:
            try:
                ArticleOldSlugs.objects.get_or_create(article=self, titre_slug=oldslug)
            except:
                pass

        if Article.objects.exclude(pk=self.pk).filter(titre_slug=slug).count() + ArticleOldSlugs.objects.exclude(article=self).filter(titre_slug=slug).count() > 0:
            slug = "%s-%s" % (slug, self.pk)
        self.titre_slug = slug
        self.save()
        
    def get_tags(self):
        tags = parse_tag_input(self.tags)
        return tags        

class ArticleOldSlugs(models.Model):
    article = models.ForeignKey(Article, related_name='article_oldslugs_set')
    titre_slug = models.SlugField(max_length=255, unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % (self.titre_slug)

class Lien(models.Model):
    titre = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    lien = models.CharField(max_length=255)
    disabled = models.BooleanField(default=False)
    ordre = models.IntegerField(default=-1)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % (self.titre)
