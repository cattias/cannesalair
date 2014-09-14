from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

register = template.Library()

@register.inclusion_tag('article/article_tags_entry.html', takes_context=True)
def article_tags_entry(context, article):
    """
    Renders a tags entry.
    """
    tagsinurl = context.get('request').GET.getlist('tag')
    tagsinarticle = article.get_tags()
    qspertag = []
    
    for t in tagsinarticle:
        qs = []
        for tiu in tagsinurl:
            if not tiu == t:
                qs.append(tiu)
        if not t in tagsinurl:
            qs.append(t)
        
        qstring = ""
        if len(qs) > 0:
            first = True
            for s in qs:
                qstring += "%stag=%s" % ("?" if first else "&", s)
                first = False
                
        qspertag.append("<a href='%s%s'>%s</a>" % (reverse("articles"), qstring, t)) 

    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'MEDIA_SERIAL': settings.MEDIA_SERIAL,
        'qspertag': qspertag,
    }
