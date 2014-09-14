from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/(?P<type>\w+)/add/$', 'comment.forms.new_comment', name='newcomment'),
    url(r'^(?P<comment_pk>\d+)/delete/$', 'comment.forms.delete_comment', name='deletecomment'),
 )