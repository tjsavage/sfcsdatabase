from django.conf.urls.defaults import *

from django.views.generic import DetailView, ListView

from django.contrib import admin
admin.autodiscover()

from database.models import Paper

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

handler500 = 'djangotoolbox.errorviews.server_error'

info_dict = {
    'queryset': Paper.objects.all(),
}

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'database.views.index'),
    (r'^database/papers/browse/$', 'database.views.browse'),
    (r'^database/papers/(?P<object_id>\d+)/$', 'database.views.paper_detail'),
    (r'^database/papers/submit/$', 'database.views.submit'),
    (r'^database/partners/$', 'database.views.partners'),
    (r'^about/$', 'database.views.about'),
    (r'^updates/$', 'database.views.news'),
    (r'^updates/(?P<object_id>\d+)/$', 'database.views.update_detail')
    
    
)

urlpatterns += staticfiles_urlpatterns()
