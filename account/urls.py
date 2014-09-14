from django.conf import settings
from django.conf.urls.defaults import patterns, url

# django.contrib
urlpatterns = patterns('',
   # Feeds
    (r'^password_reset/$', 'django.contrib.auth.views.password_reset'),
    (r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
)

urlpatterns += patterns('account.forms',
    url(r'^signup/$', 'create_new_user', name="signup"),
    url(r'^askpassword/$', 'reset_password', name="resetpassword"),
    url(r'^profil/$', 'edit_profil', name='editprofil'),
    url(r'^profil/deleteavatar/$', 'deleteavatar', name='deleteavatar'),
    url(r'^profil/mysubscriptions/$', 'edit_profil_subscriptions', name='editprofilsubscriptions'),
    url(r'^profil/changepassword/$', 'changepassword', name='changepassword'),
)

urlpatterns += patterns('account.views',
    url(r'^notification/$', 'view_notification', name='viewnotification'),
    url(r'^notification/markasread/$', 'markasread_notification', name='markasreadnotification'),
    url(r'^login/$', 'login',
        {'next_page': settings.SITE_ROOT},
        name="login"),
    url(r'^logout/$', 'logout',
        {'next_page': settings.SITE_ROOT},
        name="logout"),
    url(r'^profil/(?P<user_pk>\d+)/view/$', 'view_profil', name='viewprofil'),
)
