from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from feincms.views.cbv.views import Handler
handler = Handler.as_view()

from createjs_cms.views import PageUpdateView

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
   url(r'^createjs_cms/$', PageUpdateView.as_view(), name='page_update_view'),
)

urlpatterns += patterns('',
    url(r'^$', handler, name='feincms_home'),
    url(r'^(.*)/$', handler, name='feincms_handler'),
)
