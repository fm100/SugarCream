import os.path
from django.conf.urls.defaults import patterns, include, url
from sugarcream.views import *

from django.contrib import admin
admin.autodiscover()

site_media = os.path.join(os.path.dirname(__file__), 'site_media')

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SugarCream.views.home', name='home'),
    # url(r'^SugarCream/', include('SugarCream.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', mainpage),
    url(r'^about/$', aboutpage),
    url(r'^login/$', loginpage),
    url(r'^logout/$', logoutpage),
    url(r'^register/$', registerpage),
    url(r'^modify/$', modifypage),
    url(r'^user/$', userpage),
    url(r'^p/(\w+)/$', projectpage),
    url(r'^p/(\w+)/productbacklog/$', productbacklogpage),
    url(r'^p/(\w+)/sprintbacklog/$', sprintbacklogpage),
    url(r'^p/(\w+)/assignjob/$', assignjobpage),
    url(r'^p/(\w+)/(\w+)/(\w+)/assignjob/$', assignjob),
    url(r'^p/(\w+)/(\w+)/disassignjob/$', disassignjob),
    url(r'^p/(\w+)/userstory/$', userstorypage),
    url(r'^p/(\w+)/documents/$', documentspage),
    url(r'^p/(\w+)/meetinglog/$', meetinglogpage),
    url(r'^p/(\w+)/dailyscrumbydate/(\d{4}-\d{2}-\d{2})/$', dailyscrums),
    url(r'^p/(\w+)/dailyscrum/$', dailyscrumpage),
    url(r'^p/(\w+)/backloglist/$', backloglist),
    url(r'^p/(\w+)/backlogdetail/(\w+)/$', backlogdetail),
    url(r'^p/(\w+)/sprintbackloglist/$', sprintbackloglist),
    url(r'^myprojects/$', myprojects),
    url(r'^latestprojects/$', latestprojects),
    url(r'^notices/$',notices),
    url(r'^newproject/$', newprojectpage),
    url(r'^search/$', searchpage),
    url(r'site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': site_media}),
)
