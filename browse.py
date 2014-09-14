from django.contrib import databrowse
from django.contrib.auth.models import Group

databrowse.site.register(Group)
