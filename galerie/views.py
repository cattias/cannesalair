from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from galerie.models import Galerie, Photo, DownloadJob
from django import forms
from django.contrib.auth.models import User
from core.widgets import MediumTextInput, TextareaTiny, CustomDatePicker
from account.decorators import login_required, profil_required
from log.models import LogActivity
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.sites.models import Site
from account.models import Profil
from core.mail import add_to_maillist, internal_sendmail
from django.template.loader import render_to_string
import threading
from galerie import delete_image_from_imgur,\
    delete_album_from_imgur, sync_galerie_from_imgur
from django.core.urlresolvers import reverse
import datetime
from django.conf import settings
import os
from django.utils import simplejson
from django.core.files.uploadedfile import UploadedFile
import shutil

# Required PIL classes may or may not be available from the root namespace
# depending on the installation method used.
try:
    import Image
except ImportError:
    try:
        from PIL import Image
    except ImportError:
        raise ImportError('Photologue was unable to import the Python Imaging Library. Please confirm it`s installed and available on your current Python path.')

def list_galeries(request):
    galeries = Galerie.objects.all().order_by('-date_publication')
    years = []
    for g in galeries:
        if not g.date_publication.year in years:
            years.append(g.date_publication.year)
    year = request.GET.get("year", None)
    if not year:
        year = datetime.date.today().year
    else:
        year = int(year)
    galeries = galeries.filter(date_publication__year=year)
    return render_to_response('galerie/list_galeries.html', RequestContext(request, {
                                                                                     "galeries": galeries,
                                                                                     "years": years,
                                                                                     "year": year,
                                                                                     }))

def view_galerie(request, slug):
    galerie = get_galerie_or_404(slug)
    canbeedited = request.user == galerie.auteur or request.user.is_superuser or (galerie.sortie and request.user in [p.qui for p in galerie.sortie.participant_sortie_set.filter(statut='oui')])
    issubscribed = False
    if request.user.is_authenticated() and galerie.pk:
        issubscribed = request.user.get_profile() in galerie.galeries_suivies_set.all()
    return render_to_response('galerie/galerie_view.html', RequestContext(request, {
                                                                                     "galerie": galerie,
                                                                                     "canbeedited": canbeedited,
                                                                                     "issubscribed": issubscribed,
                                                                                     "full": True,
                                                                                     }))

class AddGalerieForm(forms.ModelForm):
    auteur = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
    titre = forms.CharField(required=True, label='Titre', widget=MediumTextInput)
    description = forms.CharField(required=True, label='Description', widget=TextareaTiny(attrs={'rows':'10', 'cols':'100'}))
    date_publication = forms.DateTimeField(required=True, label='Date de la sortie', widget=CustomDatePicker(attrs={'id':'datepicker_date_publication', 'name': 'date_publication'}))
    notification = forms.BooleanField(required=False, label=u'Ne pas envoyer de notification')
    class Meta:
        model = Galerie
        exclude = ['comments', 'imgur_id', 'titre_slug', 'is_created', 'is_intreatment', 'local_path']

class LinkGalerieForm(forms.ModelForm):
    auteur = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
    imgur_id = forms.CharField(required=True, label='Imgur ID', help_text="<p>L'ID imgur est l'identifiant de votre album Imgur.<br/>Vous pouvez copier/coller directement l'url Imgur de l'album http://imgur.com/a/js9Yy#0 ou bien seulement son identifiant, ici l'identifiant est <strong>js9Yy</strong> (sans le #0)</p>", widget=MediumTextInput)
    titre = forms.CharField(required=True, label='Titre', widget=MediumTextInput)
    description = forms.CharField(required=True, label='Description', widget=TextareaTiny(attrs={'rows':'10', 'cols':'100'}))
    date_publication = forms.DateTimeField(required=True, label='Date de la sortie', widget=CustomDatePicker(attrs={'id':'datepicker_date_publication', 'name': 'date_publication'}))
    notification = forms.BooleanField(required=False, label=u'Ne pas envoyer de notification')
    class Meta:
        model = Galerie
        exclude = ['comments', 'titre_slug', 'is_created', 'is_intreatment', 'local_path']

class GalerieForm(forms.ModelForm):
    auteur = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
    titre = forms.CharField(required=True, label='Titre', widget=MediumTextInput)
    description = forms.CharField(required=True, label='Description', widget=TextareaTiny(attrs={'rows':'10', 'cols':'100'}))
    date_publication = forms.DateTimeField(required=True, label='Date de la sortie', widget=CustomDatePicker(attrs={'id':'datepicker_date_publication', 'name': 'date_publication'}))
    class Meta:
        model = Galerie
        exclude = ['comments', 'imgur_id', 'titre_slug', 'is_created', 'is_intreatment', 'local_path']

@login_required
def link_galerie(request, template_name='galerie/galerie_link.html'):
    if request.method == 'POST': # If the form has been submitted...
        new_form = LinkGalerieForm(request.POST)
        if new_form.is_valid():
            new_galerie = new_form.save(commit=False)
            new_galerie.generate_slug()
            new_galerie.local_path = os.path.join(settings.TOUPLOAD_ROOT, new_galerie.titre_slug)
            imgur_id = new_galerie.imgur_id
            if imgur_id.startswith("http://"):
                imgur_id = imgur_id[19:]
            if imgur_id.endswith("#0"):
                imgur_id = imgur_id[:-2]
            new_galerie.imgur_id = imgur_id
            new_galerie.save()
            sync_galerie_from_imgur(new_galerie)
            if not request.POST.get('notification'):
                LogActivity.recordActivity(qui=request.user, quoi=new_galerie, comment="a publi&eacute; une nouvelle galerie : <a href='%s'>%s</a>" % (new_galerie.get_absolute_url(), new_galerie.titre))
                ThreadMail(new_galerie).start()
            # Redirect after POST
            return HttpResponseRedirect(new_galerie.get_absolute_url())
        else:
            form = new_form
    else:
        init = {}
        init['auteur'] = request.user.pk
        init['date_publication'] = datetime.datetime.now()
        form = LinkGalerieForm(initial=init)
    return render_to_response(template_name,
                              RequestContext(request,
                                             {'form': form,
                                              'full': True,
                                              }))

@login_required
def sync_galerie(request, slug):
    galerie = get_galerie_or_404(slug)
    sync_galerie_from_imgur(galerie)
    return HttpResponseRedirect(galerie.get_absolute_url())

@login_required
def add_galerie(request, template_name='galerie/galerie_add.html'):
    error = None
    if request.method == 'POST': # If the form has been submitted...
        new_form = AddGalerieForm(request.POST)
        if new_form.is_valid():
            new_galerie = new_form.save(commit=False)
            new_galerie.generate_slug()
            new_galerie.local_path = os.path.join(settings.TOUPLOAD_ROOT, new_galerie.titre_slug)
            new_galerie.save()
            if not request.POST.get('notification'):
                LogActivity.recordActivity(qui=request.user, quoi=new_galerie, comment="a publi&eacute; une nouvelle galerie : <a href='%s'>%s</a>" % (new_galerie.get_absolute_url(), new_galerie.titre))
                ThreadMail(new_galerie).start()
            # Redirect after POST
            return HttpResponseRedirect(new_galerie.get_absolute_url())
        else:
            form = new_form
    else:
        init = {}
        init['auteur'] = request.user.pk
        init['date_publication'] = datetime.datetime.now()
        form = AddGalerieForm(initial=init)
    return render_to_response(template_name,
                              RequestContext(request,
                                             {'form': form,
                                              'error': error,
                                              'full': True,
                                              }))

@login_required
def edit_galerie(request, slug, template_name='galerie/galerie_edit.html'):
    galerie = get_galerie_or_404(slug)
    canbeedited = request.user == galerie.auteur or request.user.is_superuser or (galerie.sortie and request.user in [p.qui for p in galerie.sortie.participant_sortie_set.filter(statut='oui')])
    if request.method == 'POST': # If the form has been submitted...
        new_form = GalerieForm(request.POST, instance=galerie)
        if new_form.is_valid():
            new_galerie = new_form.save(commit=False)
            new_galerie.save()
            list_images = []
            for image in new_galerie.photos_set.all():
                if request.POST.get('order_%s' % image.pk):
                    list_images.append(image.pk)
                    image.ordre = int(request.POST.get('order_%s' % image.pk))
                    image.save()
            for image_to_del in new_galerie.photos_set.exclude(pk__in=list_images):
                _internal_delete_image(request, new_galerie, image_to_del)
            # Redirect after POST
            return HttpResponseRedirect(new_galerie.get_absolute_url())
        else:
            form = new_form
    else:
        form = GalerieForm(instance=galerie)
    return render_to_response(template_name,
                              RequestContext(request,
                                             {'galerie': galerie,
                                              'form': form,
                                              'canbeedited': canbeedited,
                                              'full': True,
                                              }))

@login_required
def upload_galerie(request, slug, template_name='galerie/galerie_upload.html'):
    galerie = get_galerie_or_404(slug)
    canbeedited = request.user == galerie.auteur or request.user.is_superuser or (galerie.sortie and request.user in [p.qui for p in galerie.sortie.participant_sortie_set.filter(statut='oui')])
    nbofphotos = galerie.photos_set.all().count()
    startorder = 1
    for photo in galerie.photos_set.all().order_by("-ordre"):
        startorder = photo.ordre
        break
    if nbofphotos > startorder:
        startorder = nbofphotos
    return render_to_response(template_name,
                              RequestContext(request,
                                             {'galerie': galerie,
                                              'canbeedited': canbeedited,
                                              'startorder': startorder,
                                              'full': True,
                                              }))

def send_notification_new_galerie(galerie, template_name="galerie/mail_new_galerie.html"):
    current_site = Site.objects.get_current()
    site_name = current_site.name
    domain = current_site.domain
    maillist = []
        
    for p in Profil.objects.filter(suivre_les_galeries=True):
        add_to_maillist(maillist, p.user, galerie.auteur)

    subject = "[CAL] %s" % (galerie.titre)
    from_email = "Les Cannes A L'air <no-reply@cannesalair.fr>"

    for u in maillist:
        text = render_to_string(template_name, {'site_name': site_name,
                                                'domain': domain,
                                                'user': galerie.auteur,
                                                'galerie': galerie,
                                                'profil': u,
                                                })
        internal_sendmail(u.email, from_email, text, subject)

class ThreadMail(threading.Thread):
    def __init__(self, galerie):
        threading.Thread.__init__(self)
        self.galerie = galerie
        
    def run(self):
        send_notification_new_galerie(self.galerie)

@login_required
@profil_required
def subscribe_galerie_imgur(request, slug):
    galerie = get_galerie_or_404(slug)
    subscribe_galerie(request.user.get_profile(), galerie)
    return HttpResponseRedirect(galerie.get_absolute_url())

def subscribe_galerie(profile, galerie):
    if profile and galerie not in profile.sorties.all():
        profile.galeries.add(galerie)

@login_required
@profil_required
def unsubscribe_galerie_imgur(request, slug):
    galerie = get_galerie_or_404(slug)
    unsubscribe_galerie(request.user.get_profile(), galerie)
    next_page = request.GET.get('next_page')
    if next_page:
        return HttpResponseRedirect(next_page)
    else:
        return HttpResponseRedirect(galerie.get_absolute_url())

def unsubscribe_galerie(profile, galerie):
    if profile and galerie in profile.galeries.all():
        profile.galeries.remove(galerie)

def _internal_delete_image(request, galerie, image):
    if image.hash and galerie.imgur_id and galerie.is_created and not settings.DEBUG:
        ThreadDeleteImage(request, galerie.imgur_id, image.hash).start()
    try:
        if image.local_path and os.path.exists(image.local_path):
            os.remove(image.local_path)
        if image.thumb_local_path and os.path.exists(image.thumb_local_path):
            os.remove(image.thumb_local_path)
    except:
        pass
    image.delete()

class ThreadDeleteImage(threading.Thread):
    def __init__(self, request, imgur_id, image_hash):
        threading.Thread.__init__(self)
        self.request = request
        self.imgur_id = imgur_id
        self.image_hash = image_hash

    def run(self):
        delete_image_from_imgur(self.request, self.imgur_id, self.image_hash)

@login_required
def delete_image(request, slug, image_id):
    image = get_object_or_404(Photo, pk=image_id)
    galerie = get_galerie_or_404(slug)
    _internal_delete_image(request, galerie, image)
    return HttpResponse(str(image_id))

@login_required
def delete_galerie(request, slug):
    galerie = get_galerie_or_404(slug)
    for image in galerie.photos_set.all():
        _internal_delete_image(request, galerie, image)
    if galerie.imgur_id and galerie.is_created and not settings.DEBUG:
        delete_album_from_imgur(request, galerie.imgur_id)
    if galerie.local_path:
        galeriepath = galerie.local_path
        shutil.rmtree(galeriepath, ignore_errors=True)
    galerie.delete()
    return HttpResponseRedirect(reverse("galeries"))

@login_required
def upload_photos(request):
    if request.method == 'POST': # If the form has been submitted...
        slug = request.POST.get('slug')
        galerie = get_galerie_or_404(slug)
        if not galerie.local_path:
            galerie.local_path = os.path.join(settings.TOUPLOAD_ROOT, galerie.titre_slug)
            galerie.save()
        rootpath = galerie.local_path
            
        if not os.path.exists(rootpath):
            os.makedirs(rootpath)

        f = request.FILES.get("files")
        wrapped_file = UploadedFile(f)
        filename = wrapped_file.name
        if request.POST.get("ordre_"+filename):
            ordre = int(request.POST.get("ordre_"+filename))
        else:
            ordre = galerie.photos_set.all().count() + 1
        file_size = wrapped_file.file.size

        fullpath = os.path.join(rootpath, f.name)
        img = None
        if not os.path.exists(fullpath):
            destination = open(fullpath, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
            img = Photo(galerie=galerie, local_path=fullpath)
            img.filename = f.name
            img.filesize = file_size
            img.ordre = ordre
            img.local_url = "%s%s/%s" % (settings.TOUPLOAD_URL, galerie.titre_slug, f.name)
            img.generate_slug()
            img.save()
            resize_image_thumb(img, rootpath)

        #generating json response array
        result = []
        if img:
            result.append({"name": filename, 
                           "size": file_size, 
                           "url": img.get_imgur_url(), 
                           "thumbnail_url": img.get_thumbnail_url(),
                           "delete_url": reverse("deleteimage", kwargs={"slug": slug, "image_id": img.pk}), 
                           "delete_type":"GET",})
        response_data = simplejson.dumps(result)
        #checking for json data type
        #big thanks to Guy Shapiro
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, mimetype=mimetype)
    else: #GET
        return HttpResponse('Only POST accepted')

def get_json_galerie(request, slug):
    galerie = get_galerie_or_404(slug)
    result = []
    for img in galerie.photos_set.all():
        result.append({"name": img.filename, 
                       "size": img.filesize, 
                       "url": img.get_imgur_url(), 
                       "thumbnail_url": img.get_thumbnail_url(),
                       "delete_url": reverse("deleteimage", kwargs={"slug": slug, "image_id": img.pk}), 
                       "delete_type":"GET",})
    response_data = simplejson.dumps(result)
    #checking for json data type
    #big thanks to Guy Shapiro
    if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
        mimetype = 'application/json'
    else:
        mimetype = 'text/plain'
    return HttpResponse(response_data, mimetype=mimetype)

def resize_image_thumb(img, rootpath):
    im = Image.open(img.local_path)
    cur_width, cur_height = im.size
    new_width, new_height = (90, 90)

    ratio = max(float(new_width)/cur_width,float(new_height)/cur_height)
    x = (cur_width * ratio)
    y = (cur_height * ratio)
    xd = abs(new_width - x)
    yd = abs(new_height - y)
    x_diff = int(xd / 2)
    y_diff = int(yd / 2)
    crop_from = "bottom"
    if crop_from == 'top':
        box = (int(x_diff), 0, int(x_diff+new_width), new_height)
    elif crop_from == 'left':
        box = (0, int(y_diff), new_width, int(y_diff+new_height))
    elif crop_from == 'bottom':
        box = (int(x_diff), int(yd), int(x_diff+new_width), int(y)) # y - yd = new_height
    elif crop_from == 'right':
        box = (int(xd), int(y_diff), int(x), int(y_diff+new_height)) # x - xd = new_width
    else:
        box = (int(x_diff), int(y_diff), int(x_diff+new_width), int(y_diff+new_height))
    im = im.resize((int(x), int(y)), Image.ANTIALIAS).crop(box)
    im_filename = "thumb_%s" % img.filename
    img.thumb_local_url = "%s%s/%s" % (settings.TOUPLOAD_URL, img.galerie.titre_slug, im_filename)
    im_filename = os.path.join(rootpath, im_filename)
    im.save(im_filename, 'JPEG', quality=90, optimize=True)
    img.thumb_local_path = im_filename
    img.save()

def view_image(request, imagehash):
    photo = get_object_or_404(Photo, hash=imagehash)
    canbeedited = request.user == photo.galerie.auteur or request.user.is_superuser or (photo.galerie.sortie and request.user in [p.qui for p in photo.galerie.sortie.participant_sortie_set.filter(statut='oui')])
    return render_to_response('galerie/photo_view.html', RequestContext(request, {
                                                                                     "photo": photo,
                                                                                     "canbeedited": canbeedited,
                                                                                     "full": True,
                                                                                     }))

class DownloadGalerieForm(forms.Form):
    email = forms.EmailField(required=True, label='Email', widget=MediumTextInput)

def download_galerie(request, slug, template_name='galerie/galerie_dl.html'):
    galerie = get_galerie_or_404(slug)
    init = {}
    if request.user.is_authenticated() and request.user.email:
        init = {'email': request.user.email,}
        
    form = DownloadGalerieForm(initial=init)
    if request.method == 'POST': # If the form has been submitted...
        ids = request.POST.getlist("imageid")
        if ids:
            form = DownloadGalerieForm(request.POST)
            if form.is_valid():
                job = DownloadJob(galerie=galerie, email=request.POST.get('email'))
                job.save()
                for pk in ids:
                    image = Photo.objects.get(pk=pk)
                    job.images.add(image)
                return HttpResponseRedirect(reverse("downloadendgalerie", kwargs={"slug": slug,}))
    return render_to_response(template_name,
                              RequestContext(request,
                                             {'galerie': galerie,
                                              'form': form,
                                              'full': True,
                                              }))

def downloadend_galerie(request, slug, template_name='galerie/galerie_dl_end.html'):
    galerie = get_galerie_or_404(slug)
    return render_to_response(template_name,
                              RequestContext(request,
                                             {'galerie': galerie,
                                              'full': True,
                                              }))

@login_required
def update_photos(request, slug, template_name='galerie/galerie_up_photos.html'):
    galerie = get_galerie_or_404(slug)
    canbeedited = request.user == galerie.auteur or request.user.is_superuser or (galerie.sortie and request.user in [p.qui for p in galerie.sortie.participant_sortie_set.filter(statut='oui')])
    if request.method == 'POST':
        images = request.POST.getlist('image')
        for imageid in images:
            image = Photo.objects.get(pk=int(imageid))
            titre = request.POST.get('titre_%s' % imageid)
            if titre == "Titre":
                titre = None
            description = request.POST.get('description_%s' % imageid)
            if description == "Description":
                description = None
            image.titre = titre
            image.description = description
            image.generate_slug()
            image.save()
        return HttpResponseRedirect(galerie.get_absolute_url())
    return render_to_response(template_name,
                              RequestContext(request,
                                             {'galerie': galerie,
                                              'canbeedited': canbeedited,
                                              'full': True,
                                              }))

def get_galerie_or_404(slug):
    galerie = None
    try:
        galerie = Galerie.objects.get(titre_slug=slug)
    except Galerie.DoesNotExist:
        try:
            galerie = Galerie.objects.get(imgur_id=slug)
        except Galerie.DoesNotExist:
            try:
                galerie = Galerie.objects.get(pk=int(slug))
            except:
                raise Http404("La galerie n'existe pas")
    return galerie
