from django.conf.urls.defaults import *

from django.views.generic import DetailView, ListView
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from database.models import Paper

import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns


info_dict = {
    'queryset': Paper.objects.all(),
}

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'database.views.index'),
    (r'^database/papers/browse/$', 'database.views.browse'),
    (r'^database/papers/search/$', 'database.views.search'),
    (r'^database/papers/(?P<object_id>\d+)/$', 'database.views.paper_detail'),
    (r'^database/papers/(?P<object_id>\d+)/download/$', 'database.views.paper_download'),
    (r'^database/papers/(?P<object_id>\d+)/comment/$', 'database.views.paper_comment'),
    (r'^database/papers/submit/$', 'database.views.submit'),
    (r'^database/authors/(?P<object_id>\d+)/$', 'database.views.author_detail'),
    (r'^database/partners/$', 'database.views.partners'),
    (r'^about/$', direct_to_template, {
        'template' : 'about.html'
    }),
    (r'^updates/$', 'database.views.updates'),
    (r'^updates/(?P<object_id>\d+)/$', 'database.views.update_detail'),
    
    
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    from django.views.static import serve
    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns += patterns('',
            (r'^%s(?P<path>.*)$' % _media_url,
            serve,
            {'document_root': settings.MEDIA_ROOT}))
        del(_media_url, serve)