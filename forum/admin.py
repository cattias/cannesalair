from django.contrib import admin
from forum.models import Groupe, Forum, Thread, Message

admin.site.register(Groupe)
admin.site.register(Forum)
admin.site.register(Thread)
admin.site.register(Message)
