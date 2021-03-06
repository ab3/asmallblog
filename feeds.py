from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.utils import feedgenerator
from django.core.exceptions import ObjectDoesNotExist
from models import Entry, Comment, Tag
from datetime import datetime, time

class LatestEntries(Feed):
    feed_type = feedgenerator.Rss201rev2Feed
    
    title = 'Abeocracy.be'
    link = 'http://abeocracy.be'
    description = 'The latest entries from abeocracy.be'
    
    def items(self):
        return Entry.objects.filter(listed=True)[:10]
    
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


class LatestEntriesByTag(Feed):
    feed_type = feedgenerator.Rss201rev2Feed
    
    title = 'Abeocracy.be'
    link = 'http://abeocracy.be'
    description = 'The latest entries from abeocracy.be'
    
    def get_object(self, request, tag):
        if len(tag) != 1:
            raise ObjectDoesNotExist
        return Tag.objects.get(listed=True, title=tag[0].title)
                
    def items(self, obj):
        return Entry.objects.filter(listed=True, category_title=obj)[:10]
    
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

class LatestComments(Feed):
    feed_type = feedgenerator.Rss201rev2Feed

    title = 'Abeocracy.be'
    link = 'http://abeocracy.be'
    description = 'The latest comments from abeocracy.be'

    def items(self):
        return Comment.objects.filter()[:10]

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
