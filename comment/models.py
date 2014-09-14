from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Comment(models.Model):
    auteur = models.ForeignKey(User, related_name='comment_auteur_set')
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s - %s" % (self.auteur.username, self.date_publication)


    def get_article(self):
        a = None
        if self.article_comments_set.all().count() > 0:
            a = self.article_comments_set.all()[0]
        return a

    def get_sortie(self):
        s = None
        if self.sortie_comments_set.all().count() > 0:
            s = self.sortie_comments_set.all()[0]
        return s

    def get_galerie(self):
        g = None
        if self.galerie_comments_set.all().count() > 0:
            g = self.galerie_comments_set.all()[0]
        return g

    def get_ref_url(self):
        a = self.get_article()
        s = self.get_sortie()
        g = self.get_galerie()
        if a:
            return a.get_absolute_url()
        if s:
            return s.get_absolute_url()
        if g:
            return g.get_absolute_url()
        return reverse("root")
    
    def get_ref_titre(self):
        t = None
        a = self.get_article()
        s = self.get_sortie()
        g = self.get_galerie()
        if a:
            t = a.titre
        if s:
            t = s.titre
        if g:
            t = g.titre
        return t

    def get_ref_type(self):
        t = None
        a = self.get_article()
        s = self.get_sortie()
        g = self.get_galerie()
        if a:
            t = "Article"
        if s:
            t = "Activit&eacute;"
        if g:
            t = "Galerie"
        return t
