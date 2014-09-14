# -*- coding: utf-8 -*-
"""
Forms for meteo
"""
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.contrib.auth.models import User
from core.widgets import TextareaTiny, CustomDatePicker
from account.decorators import login_required
from meteo.models import Prevision
from meteo.views import internal_view_previ
from django.contrib.auth.decorators import permission_required

class PreviForm(forms.ModelForm):
    auteur = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
    date_previ = forms.DateTimeField(required=True, label=u'Date de la prévision', widget=CustomDatePicker(attrs={'id':'datepicker_date_previ', 'name': 'date_previ'}))
    description = forms.CharField(required=True, label='Description', widget=TextareaTiny(attrs={'rows':'10', 'cols':'100'}))
    sources = forms.CharField(required=False, label='Sources', widget=TextareaTiny(attrs={'rows':'5', 'cols':'100'}))
    annexe = forms.CharField(required=False, label='Annexe', widget=TextareaTiny(attrs={'rows':'10', 'cols':'100'}))

    class Meta:
        model = Prevision
        fields = ['auteur', 'date_previ', 'description', 'sources', 'annexe']

@login_required
@permission_required('account.can_view_secure_files')
def add_previ(request, template_name='meteo/previ_add.html'):
    if request.method == 'POST': # If the form has been submitted...
        preview = request.POST.get('preview', None)
        editpreview = request.POST.get('editpreview', None)
        new_form = PreviForm(request.POST)
        if not editpreview and new_form.is_valid():
            new_previ = new_form.save(commit=False)
            if not preview:
                new_previ.save()
                # Redirect after POST
                return HttpResponseRedirect(new_previ.get_absolute_url())
            else:
                return internal_view_previ(request, new_previ, urlretour=reverse("addprevi"))
        else:
            form = new_form
    else:
        init = {}
        init['auteur'] = request.user.pk
        form = PreviForm(initial=init)
    return render_to_response(template_name,
                              RequestContext(request,
                                             {'form': form,
                                              'full': True,
                                              }))

@login_required
def edit_previ(request, previid, template_name='meteo/previ_edit.html'):
    previ = Prevision.objects.get(pk=previid)
    if request.method == 'POST': # If the form has been submitted...
        preview = request.POST.get('preview', None)
        editpreview = request.POST.get('editpreview', None)
        new_form = PreviForm(request.POST, instance=previ)
        if not editpreview and new_form.is_valid():
            new_previ = new_form.save(commit=False)
            if not preview:
                new_previ.save()
                # Redirect after POST
                return HttpResponseRedirect(previ.get_absolute_url())
            else:
                return internal_view_previ(request, new_previ, urlretour=reverse("editprevi", kwargs={"previid": previid}))
        else:
            form = new_form
    else:
        form = PreviForm(instance=previ)
    return render_to_response(template_name,
                              RequestContext(request,
                                             {'form': form,
                                              'previ': previ,
                                              'full': True,
                                              }))

@login_required
def delete_previ(request, previid):
    previ = Prevision.objects.get(pk=previid)
    if previ:
        previ.delete()
    return HttpResponseRedirect(reverse("listprevi"))

