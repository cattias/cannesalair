from django.contrib import admin
from article.models import Article, ArticleOldSlugs, Lien

admin.site.register(Article)
admin.site.register(ArticleOldSlugs)
admin.site.register(Lien)
