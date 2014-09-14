# -*- coding: utf-8 -*-
from photologue.models import Gallery, Photo
from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.conf import settings
from photologue.urls import SAMPLE_SIZE

def list_galleries(request, template_name='photologue/gallery_list.html'):
    galleries = Gallery.objects.filter(is_public=True).order_by('-date_added')
    galleriescount = len(galleries)

    paginator = Paginator(galleries, settings.PAGE_COUNT_SIZE)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        galleries = paginator.page(page)
    except (EmptyPage, InvalidPage):
        galleries = paginator.page(paginator.num_pages)

    return render_to_response(template_name,
                              RequestContext(request,
                                             {
                                              'galleries': galleries,
                                              'galleriescount': galleriescount,
                                              'paginator': paginator,
                                              'sample_size': SAMPLE_SIZE,
                                              }))

def view_gallery(request, slug, template_name='photologue/gallery_detail.html'):
    gallery = get_object_or_404(Gallery, title_slug=slug)
    return render_to_response(template_name,
                              RequestContext(request,
                                             {
                                              'gallery': gallery,
                                              'sample_size': SAMPLE_SIZE,
                                              'full': True,
                                              }))

def view_photo(request, slug, template_name='photologue/photo_detail.html'):
    photo = get_object_or_404(Photo, title_slug=slug)
    return render_to_response(template_name,
                              RequestContext(request,
                                             {
                                              'photo': photo,
                                              'sample_size': SAMPLE_SIZE,
                                              'full': True,
                                              }))
