from django.conf.urls.defaults import *
from asmallblog import views, feeds

feeds = {
    'latest': feeds.LatestEntries
}

urlpatterns = patterns('',
    # A Small Blog urls
    url(r'^$', views.index, name='asb-index-default'),
    url(r'^(?P<entry_slug>[\w-]+)/$', views.entry, name='asb-entry'),
    url(r'^tag/$', views.tags, name='asb-tags'),
    url(r'^tag/(?P<tag_title>[\w-]+)/$', views.tag, name='asb-tag'),
    url(r'^date/$', views.date, name='asb-date'),
    url(r'^date/(?P<year>\d{4})/$', views.date, name='asb-date'),
    url(r'^date/(?P<year>\d{4})/(?P<month>\d{2})/$', views.date, name='asb-date'),
    url(r'^date/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.date, name='asb-date'),
    
    # A Small Blog Feeds
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)