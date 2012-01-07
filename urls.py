from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login as loginpage
from sugarcream.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SugarCream.views.home', name='home'),
    # url(r'^SugarCream/', include('SugarCream.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', mainpage),
    url(r'^login/$', loginpage),
    url(r'^logout/$', logoutpage),
    url(r'^register/$', registerpage),
    url(r'^user/(\w+)/$', userpage),
    url(r'^p/(\w+)/$', projectpage),
)
