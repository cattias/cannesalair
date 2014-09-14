from admin.management.sites import init_siteconfig
from django.db.models import signals


signals.post_syncdb.connect(init_siteconfig)
