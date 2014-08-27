from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
from MusicHandler import settings

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'auth/', include('authentication.urls', namespace='authentication')),
                       url(r'media/', include('media.urls', namespace='media')),
                       (r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
