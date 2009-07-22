from django.conf.urls.defaults import *
from dquiz.vocab import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Show a quiz - start with a quiz_id and if needed specify the page
    url(r'^quiz/(?P<quiz_id>\d+)/(?P<page>\d+)?$', views.quiz, name='vocab-quiz'),
    url(r'^quiz/(?P<quiz_id>\d+)/(?P<page>\d+)/(?P<def_id>\d+)/answer$', views.answer, name='vocab-answer'),

	# Add words
	url(r'^add/?$', views.add, name='vocab-add'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

	#Static content
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
)
