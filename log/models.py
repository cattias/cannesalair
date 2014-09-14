from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

class LogActivity(models.Model):
    qui = models.ForeignKey(User, related_name='log_qui_set')
    contenu = models.TextField()
    type = models.ForeignKey(ContentType, related_name='log_type_set', blank=True, null=True)
    object_id = models.IntegerField(blank=True, null=True)
    related_type = models.ForeignKey(ContentType, related_name='log_related_type_set', blank=True, null=True)
    related_object_id = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s %s" % (self.qui.username, self.contenu)

    @staticmethod
    def getDefault():
        act = LogActivity.objects.all().order_by("-pk")[0]
        return act

    @staticmethod
    def recordActivity(qui, quoi, comment, surquoi=None):
        la = LogActivity(qui=qui, contenu=comment, type=ContentType.objects.get_for_model(quoi), object_id=quoi.pk)
        if surquoi:
            la.related_type = ContentType.objects.get_for_model(surquoi)
            la.related_object_id = surquoi.pk
        la.save()
#        p = qui.get_profile()
#        p.last_known_activity = la
#        p.save()