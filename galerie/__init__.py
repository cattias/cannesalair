from django.conf import settings
import requests
import json
import base64
import os
import logging

def get_imgur_cookie(request):
    cookie = None
    if "imgur_cookie" in request.session:
        cookie = request.session["imgur_cookie"]
    else:
        cookie = _internal_get_imgur_cookie()
        request.session["imgur_cookie"] = cookie
    return cookie

def _internal_get_imgur_cookie():
    auth = dict(username=settings.IMGUR_ACCOUNT, password=settings.IMGUR_PASSWORD, remember='remember', submit='')
    r = requests.post(settings.IMGUR_SIGNIN_URL, data=auth)
    return r.cookies

def get_json_album(request, imgur_id):
    cookies = get_imgur_cookie(request)
    return _internal_get_json_album(cookies, imgur_id)

def _internal_get_json_album(cookies, imgur_id):
    url = get_imgur_url_for_action_anon('album/%s' % imgur_id)
    page = 0
    result = []
    boucle = True
    while boucle:
        page+=1
        r = requests.get(url+"?count=100&page="+str(page), cookies=cookies)
        resulttemp = []
        if r.ok:
            resulttemp = json.loads(r.content)['album']['images']
            result.extend(resulttemp)
        boucle = r.ok and len(resulttemp) == 100
    return result

def get_imgur_url_for_action(action):
    d = dict(endpoint=settings.IMGUR_API_ENDPOINT, version=settings.IMGUR_API_VERSION, account=settings.IMGUR_API_ACCOUNT, action=action, format=settings.IMGUR_API_FORMAT)
    return "%(endpoint)s/%(version)s/%(account)s/%(action)s.%(format)s" % d

def get_imgur_url_for_action_anon(action):
    d = dict(endpoint=settings.IMGUR_API_ENDPOINT, version=settings.IMGUR_API_VERSION, action=action, format=settings.IMGUR_API_FORMAT)
    return "%(endpoint)s/%(version)s/%(action)s.%(format)s" % d

def create_album(title):
    cookies = _internal_get_imgur_cookie()
    imgur_id = None
    data = dict(title=title, description='Automatic album creation from CAL website', privacy='public', layout='grid')
    url = get_imgur_url_for_action('albums')
    r = requests.post(url, data=data, cookies=cookies)
    if r.ok:
        imgur_id = json.loads(r.content).get('albums').get("id")
    return imgur_id

def delete_image_from_imgur(request, imgur_id, image_id):
    cookies = get_imgur_cookie(request)
    url = get_imgur_url_for_action('images/%s' % image_id)
    requests.delete(url, cookies=cookies)
    data = dict(del_images=image_id)
    requests.post(get_imgur_url_for_action('albums/%s' % imgur_id), data=data, cookies=cookies)

def delete_album_from_imgur(request, imgur_id):
    cookies = get_imgur_cookie(request)
    url = get_imgur_url_for_action('albums/%s' % imgur_id)
    requests.delete(url, cookies=cookies)

def upload_image_to_imgur_album(image):
    logger = logging.getLogger('uploader')
    image.is_intreatment = True
    image.save()
    cookies = _internal_get_imgur_cookie()
    imagefile = open(image.local_path, 'rb')
    data = dict(image=base64.b64encode(imagefile.read()))
    result = True
    # Upload
    try:
        resp = requests.post(get_imgur_url_for_action('images'), data=data, cookies=cookies)
        if resp.ok:
            image_id = json.loads(resp.content).get('images').get("image").get("hash")
            image.hash = image_id
            image.is_uploaded = True
            image.save()

            # Remove local files
            imagefile.close()
            os.remove(image.local_path)
            os.remove(image.thumb_local_path)
            parent_dir = os.path.abspath(os.path.join(image.local_path, os.path.pardir))
            if len(os.listdir(parent_dir)) == 0:
                os.rmdir(parent_dir)
            image.local_path = None
            image.local_url = None
            image.thumb_local_path = None
            image.thumb_local_url = None
            image.save()

            # Link to galerie
            result = link_image_to_imgur_album(image)
        else:
            logger.error("%s - Erreur pendant l'upload - %s - %s (url=%s)" % (image.filename, resp.status_code, resp.error, resp.url))
            result = False
    except Exception, ex:
        logger.error("%s - Erreur pendant l'upload - %s" % (image.filename, str(ex)))
        result = False
        
    image.is_intreatment = False
    image.save()
    return result

def link_image_to_imgur_album(image):
    logger = logging.getLogger('uploader')
    image.is_intreatment = True
    image.save()
    cookies = _internal_get_imgur_cookie()
    data = dict(add_images=image.hash, cover=image.hash)
    result = True
    # Link to galerie
    if image.galerie.is_created and image.galerie.imgur_id:
        try:
            resp = requests.post(get_imgur_url_for_action('albums/%s' % image.galerie.imgur_id), data=data, cookies=cookies)
            if resp.ok:
                image.is_linked = True
                image.save()
                result = True
            else:
                logger.error("%s - Erreur pendant le link avec la galerie" % image.filename)
                result = False
        except:
            logger.error("%s - Erreur pendant le link avec la galerie" % image.filename)
            result = False
    else:
        logger.error("%s - La galerie n'existe pas sur imgur" % image.filename)
        result = False
        
    image.is_intreatment = False
    image.save()
    return result

def sync_galerie_from_imgur(galerie, request=None):
    if galerie.imgur_id and galerie.is_created:
        from galerie.models import Photo
        cookies = None
        if request:
            cookies = get_imgur_cookie(request)
        else:
            cookies = _internal_get_imgur_cookie()
        images = _internal_get_json_album(cookies, galerie.imgur_id)
        i=1
        list_hash = []
        for image in images:
            img = Photo.objects.get_or_create(hash=image['image']['hash'], galerie=galerie)[0]
            img.is_uploaded=True
            if img.ordre==0:
                img.ordre=i
            img.date_publication=galerie.date_publication
            if not img.filename:
                img.filename = "%s.jpg" % image['image']['hash']
            img.filesize = int(image['image']['size'])
            img.save()
            list_hash.append(img.hash)
            i+=1
        
        for image in galerie.photos_set.exclude(hash__in=list_hash):
            image.delete()
