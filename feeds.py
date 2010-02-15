from django.contrib.syndication.feeds import Feed
from django.utils import feedgenerator
from models import Entry
from datetime import datetime, time

class LatestEntries(Feed):
    feed_type = feedgenerator.Rss201rev2Feed
    
    title = 'Abeocracy.be'
    link = 'http://abeocracy.be'
    description = 'The latest entries from abeocracy.be'
    # subtitle = 'The latest entries from abeocracy.be'
    
    def items(self):
        return Entry.objects.filter(listed=True)[:10] #order_by('-pub_date')[:10]
    
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.text
    
    def item_link(self, item):
        return item.get_absolute_url()
    
    def item_pubdate(self, item):
        return item.pub_date
        
    def item_categories(self, item):
        return item.tags.all()