from django import template
from django.conf import settings
from sortie.models import Participant, SpecialParticipant
from django.template.defaultfilters import stringfilter
from django.core.urlresolvers import reverse

register = template.Library()

@register.filter(name='statut')
@stringfilter
def statut(value):
    return dict(Participant.STATUT)[value]

@register.inclusion_tag('sortie/sortie_entry.html', takes_context=True)
def sortie_entry(context, sortie, counter=None, show=None):
    """
    Renders a sortie entry.
    """
    user = context.get('user', None)
    perms = context.get('perms', None)
    statut = None
    pp = None
    if user.is_authenticated():
        pp =  Participant.objects.filter(qui=user, sortie=sortie)
    participant = None
    if pp and pp.count() > 0:
        participant = pp[0]
    if participant:
        statut = participant.statut

    raw_type = sortie.typesortie.code
    typesortie = sortie.typesortie.name

    poui = Participant.objects.filter(sortie=sortie, statut="oui")
    ppe = Participant.objects.filter(sortie=sortie, statut="peutetre")
    pnon = Participant.objects.filter(sortie=sortie, statut="non")
    
    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'MEDIA_SERIAL': settings.MEDIA_SERIAL,
        'sortie': sortie,
        'statut': statut,
        'type': typesortie,
        'raw_type': raw_type,
        'counter': counter,
        'show': show,
        'user': user,
        'perms': perms,
        'poui': poui,
        'ppe': ppe,
        'pnon': pnon,
    }

@register.inclusion_tag('sortie/special_participation_entry.html', takes_context=True)
def special_participation_entry(context, sortie, qui, status):
    """
    Renders a sortie special participation entry.
    """
    user = context.get('user', None)
    perms = context.get('perms', None)
    sp = SpecialParticipant.objects.filter(sortie=sortie, qui=qui, status=status)
    
    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'MEDIA_SERIAL': settings.MEDIA_SERIAL,
        'sortie': sortie,
        'qui': qui,
        'sp': sp,
        'user': user,
        'perms': perms,
    }

@register.inclusion_tag('sortie/sortie_resume_entry.html', takes_context=True)
def sortie_resume_entry(context, sortie, color):
    """
    Renders a sortie resume entry.
    """
    user = context.get('user', None)
    perms = context.get('perms', None)
    totalpe = sortie.participant_sortie_set.filter(statut='peutetre').count() + sortie.participant_special_sortie_set.filter(statut='peutetre').count()
    totalsur = sortie.participant_sortie_set.filter(statut='oui').count() + sortie.participant_special_sortie_set.filter(statut='oui').count()
    totalfull = totalpe + totalsur
    
    dureesortie = None
    if not sortie.date_debut.date == sortie.date_fin.date:
        dureesortie = sortie.date_fin - sortie.date_debut
        dureesortie = dureesortie.days + 1
        if dureesortie == 1:
            dureesortie = None

    maparticipation = None
    if user.is_authenticated():
        maparticipation = Participant.objects.filter(qui=user, sortie=sortie)
        if maparticipation.count() > 0:
            maparticipation = maparticipation[0]
        else:
            maparticipation = None
        
    tagsinurl = context.get('request').GET.getlist('cat')
    tagsinsortie = [a.activite for a in sortie.activites.all()]
    qspertag = []
    for t in tagsinsortie:
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
                qstring += "%scat=%s" % ("?" if first else "&", s)
                first = False
                
        qspertag.append("<a href='%s%s'>%s</a>" % (reverse("sorties"), qstring, t))
    
    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'MEDIA_SERIAL': settings.MEDIA_SERIAL,
        'sortie': sortie,
        'totalfull': totalfull,
        'totalpe': totalpe,
        'totalsur': totalsur,
        'color': color,
        'dureesortie': dureesortie,
        'maparticipation': maparticipation,
        'user': user,
        'perms': perms,
        'qspertag': qspertag,
    }

@register.inclusion_tag('sortie/sortie_cats_entry.html', takes_context=True)
def sortie_categories_entry(context, sortie):
    """
    Renders a sortie resume entry.
    """
    user = context.get('user', None)
    perms = context.get('perms', None)
    
    tagsinurl = context.get('request').GET.getlist('cat')
    tagsinsortie = [a.activite for a in sortie.activites.all()]
    qspertag = []
    for t in tagsinsortie:
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
                qstring += "%scat=%s" % ("?" if first else "&", s)
                first = False
                
        qspertag.append("<a href='%s%s'>%s</a>" % (reverse("sorties"), qstring, t)) 
    
    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'MEDIA_SERIAL': settings.MEDIA_SERIAL,
        'user': user,
        'perms': perms,
        'qspertag': qspertag,
    }
