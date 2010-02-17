from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.db.models import Count, F
from models import Tag, Entry, Comment
from forms import PartialCommentForm

PAGE_ENTRY_COUNT = 5

def entries(request, entries_list, tag=None):
    entries_list = entries_list.annotate(comment_count=Count('comment'))
    paginator = Paginator(entries_list, PAGE_ENTRY_COUNT)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
        
    try:
        entries_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        entries_list = paginator.page(paginator.num_pages)
        
    return render_to_response('asmallblog/index.html', {'request': request, 'entries_list': entries_list.object_list, 'page': entries_list, 'tag': tag})


def index(request):
    entries_list = Entry.objects.filter(listed=True)
    
    return entries(request, entries_list)


def tag(request, tag_title, page=1):
    t = get_object_or_404(Tag, title=tag_title)
    entries_list = Entry.objects.filter(listed=True, tags=t)
    paginator = Paginator(entries_list, PAGE_ENTRY_COUNT)

    return entries(request, entries_list, t)


def date(request, year=None, month=None, day=None):
    if not year:
        entries_list = Entry.objects.filter(listed=True)
    elif not month:
        entries_list = Entry.objects.filter(listed=True, pub_date__year=year)
    elif not day:
        entries_list = Entry.objects.filter(listed=True, pub_date__year=year, pub_date__month=month)
    else:
        entries_list = Entry.objects.filter(listed=True, pub_date__year=year, pub_date__month=month, pub_date__day=day)

    return entries(request, entries_list)


def entry(request, entry_slug):
    e = get_object_or_404(Entry, slug=entry_slug)
    comments_list = Comment.objects.filter(entry=e)
    if request.method == 'POST':
        c = Comment(entry=e)
        form = PartialCommentForm(request.POST, instance=c)
        if form.is_valid():
            form.save()
            form = PartialCommentForm()
            HttpResponseRedirect(reverse('asb-entry', args=(e.slug,)))
    else:
        form = PartialCommentForm()
    
    return render_to_response('asmallblog/entry_details.html', {'entry': e, 'comments': comments_list, 'form': form})


def tags(request):
    tags_list = Tag.objects.all()
    return render_to_response('asmallblog/tags.html', {'tags': tags_list})