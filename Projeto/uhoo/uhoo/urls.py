from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BlogS.views.home', name='home'),
    # url(r'^BlogS/', include('BlogS.foo.urls')),

    url(r'^comments/', include('django.contrib.comments.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^galeria/', include('image_gal.urls')),
    (r'^relships/', include('relships.urls')),
    (r'^media/(.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
)


urlpatterns += staticfiles_urlpatterns()
