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
    url(r'^login/$', loginpage),
    url(r'^logout/$', logoutpage),
    url(r'^register/$', registerpage),
    url(r'^user/$', userpage),
    url(r'^p/(\w+)/$', projectpage),
    url(r'^myprojects/$', myprojects),
    url(r'^allprojects/$', allprojects),
    url(r'^notices/$',notices),
    url(r'^newproject/$', newprojectpage),
    url(r'site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': site_media}),
)
