import re
from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def underscore_slugify(value):
    """
    Custom slugify'er that uses '_' instaed of '-' and
    sets the first character of a word in uppercase.
    """
    import unicodedata
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s_()]', '', value).strip())
    return mark_safe(re.sub('[_\s]+', '_', value))
underscore_slugify.is_safe = True