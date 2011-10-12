from datetime import datetime
from django.db.models import Model, CharField, TextField, IntegerField, DateTimeField, EmailField, URLField, \
    SlugField, BooleanField, ForeignKey, ManyToManyField, permalink
from django.contrib.auth.models import User


class Tag(Model):
    title = CharField(max_length=80, unique=True)
    description = TextField()
    
    class Meta:
        db_table = 'asb_tags'
    
    def __unicode__(self):
        return self.title
    
    @permalink
    def get_absolute_url(self):
        return ('asb-entry', [self.slug])
    

class Entry(Model):
    title = CharField(max_length=200)
    slug = SlugField(max_length=200, unique=True)
    pub_date = DateTimeField(default=datetime.now())
    author = ForeignKey(User)
    text = TextField(help_text='Use markdown syntax')
    tags = ManyToManyField(Tag, blank=True)
    enable_comments = BooleanField(default=True)
    listed = BooleanField(default=True,
        help_text='If enabled, this entries will appear in the entrie overview')
    
    class Meta:
        db_table = 'asb_entries'
        verbose_name_plural = 'entries' 
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'
    
    def __unicode__(self):
        return self.title
    
    
    def get_absolute_url(self):
        return ('asb-tag', [self.slug])
    
    def save(self):
        if not self.id:
            unique_slug(self, "title", "slug")
        super(Entry, self).save()


class Comment(Model):
    author = CharField(max_length=80)
    email = EmailField(blank=True)
    site = URLField(verify_exists=False, blank=True)
    pub_date = DateTimeField(default=datetime.now())
    text = TextField()
    hidden = BooleanField(default=False)
    entry = ForeignKey(Entry)
    
    class Meta:
        db_table = 'asb_comments'
        ordering = ('-pub_date',)
        verbose_name_plural = 'comments'
    
    def __unicode__(self):
        return '%s - %s' % (self.author, self.text[:25])


def unique_slug(item, slug_source, slug_field):
    """
    Ensures a unique slug populats the slug_field of item.
    When there is no slug, one will be generaded fron slug_source.
    """
    if not getattr(item, slug_field): # if it's already got a slug, do nothing.
        from filters import underscore_slugify
        reserved_pages = ('admin', 'category', 'tag', 'page', 'date', 'feeds') # see the urls.py files
        slug = underscore_slugify(getattr(item, slug_source))
        model = item.__class__
        slugs = [sl.values()[0] for sl in model.objects.values(slug_field)]
        slugs.extend(reserved_pages)
        if slug in slugs:
            import re
            counter = 2
            counter_finder = re.compile(r'_\d+$') # finds the 'slug counter' at the end of the slug
            slug = "%s_%i" % (slug, counter)
            while slug in slugs:
                slug = re.sub(counterFinder, "_%i" % counter, slug)
                counter += 1
        setattr(item, slug_field, slug) 
