from models import Tag, Entry, Comment
from django.contrib.admin import ModelAdmin, StackedInline
from django.contrib import admin


class TagAdmin(ModelAdmin):
    verbose_name = 'Tags'


class CommentAdmin(ModelAdmin):
    model = Comment
    

class CommentInline(StackedInline):
    model = Comment
    extra = 3


class EntryAdmin(ModelAdmin):
    list_display = ('title', 'pub_date')
    search_fields = ['title', 'text']
    date_hierarchy = 'pub_date'
    #prepopulated_fields = {'slug': ('title',)}
    exclude = ('slug',)
    inlines = [CommentInline]


admin.site.register(Tag, TagAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Comment, CommentAdmin)
