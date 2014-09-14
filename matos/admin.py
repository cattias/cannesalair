from django.contrib import admin
from matos.models import Categorie, Matos, Emprunt, SousCategorie

admin.site.register(Categorie)
admin.site.register(SousCategorie)
admin.site.register(Matos)
admin.site.register(Emprunt)
