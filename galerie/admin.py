from django.contrib import admin
from galerie.models import Galerie, Photo, DownloadJob

class GalerieAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'is_created', 'imgur_id', 'sortie', 'date_publication')
    search_fields = ['titre', 'description', 'imgur_id', 'auteur', 'sortie']
    list_filter = ('auteur', 'is_created', )

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('titre', 'is_uploaded', 'is_linked', 'hash', 'galerie', 'filename', 'filesize', 'ordre')
    search_fields = ['titre', 'description', 'filename', 'hash']
    list_filter = ('galerie', 'is_uploaded', 'is_linked',)

admin.site.register(Galerie, GalerieAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(DownloadJob)
