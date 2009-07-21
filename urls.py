from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Show a quiz - start with a quiz_id and if needed specify the page
    (r'^quiz/(?P<quiz_id>\d+)/?(?P<page>\d+)?', 'dquiz.vocab.views.quiz'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

	#Static content
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
)
