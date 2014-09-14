from django.contrib import admin
from sortie.models import Activite, Sortie, SortieOldSlugs, SpecialParticipant,\
    CRSortie

admin.site.register(Activite)
admin.site.register(Sortie)
admin.site.register(SortieOldSlugs)
admin.site.register(SpecialParticipant)
admin.site.register(CRSortie)
