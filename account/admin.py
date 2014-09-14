from django.contrib import admin
from account.models import Profil
from django.contrib.auth.models import Group, User

class MembershipInline(admin.TabularInline):
    model = User.groups.through

class GroupAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('permissions',)
    inlines = [
        MembershipInline,
    ]

admin.site.register(Profil)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
