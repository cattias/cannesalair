from django.http import HttpResponseRedirect, Http404, HttpResponseNotModified,\
    HttpResponse
from django.core.urlresolvers import reverse
from subprocess import Popen
import urllib
import posixpath
import os
from django.views.static import directory_index, was_modified_since
import mimetypes
from django.utils.http import http_date
from account.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.utils import simplejson

def hgpullu(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        cmd = ["hg", "pull", "-u"]
        Popen(cmd)
    return HttpResponseRedirect(reverse("root"))

@login_required
@permission_required('account.can_view_secure_files')
def serve(request, path, document_root=None, show_indexes=False):
    """
    Serve static files below a given point in the directory structure.

    To use, put a URL pattern such as::

        (r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root' : '/path/to/my/files/'})

    in your URLconf. You must provide the ``document_root`` param. You may
    also set ``show_indexes`` to ``True`` if you'd like to serve a basic index
    of the directory.  This index view will use the template hardcoded below,
    but if you'd like to override it, you can create a template called
    ``static/directory_index.html``.
    """
    path = posixpath.normpath(urllib.unquote(path))
    path = path.lstrip('/')
    newpath = ''
    for part in path.split('/'):
        if not part:
            # Strip empty path components.
            continue
        drive, part = os.path.splitdrive(part)
        head, part = os.path.split(part)
        if part in (os.curdir, os.pardir):
            # Strip '.' and '..' in path.
            continue
        newpath = os.path.join(newpath, part).replace('\\', '/')
    if newpath and path != newpath:
        return HttpResponseRedirect(newpath)
    fullpath = os.path.join(document_root, newpath)
    if os.path.isdir(fullpath):
        if show_indexes:
            return directory_index(newpath, fullpath)
        raise Http404("Directory indexes are not allowed here.")
    if not os.path.exists(fullpath):
        raise Http404('"%s" does not exist' % fullpath)
    # Respect the If-Modified-Since header.
    statobj = os.stat(fullpath)
    mimetype, encoding = mimetypes.guess_type(fullpath)
    mimetype = mimetype or 'application/octet-stream'
    if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                              statobj.st_mtime, statobj.st_size):
        return HttpResponseNotModified(mimetype=mimetype)
    response = HttpResponse(open(fullpath, 'rb').read(), mimetype=mimetype)
    response["Last-Modified"] = http_date(statobj.st_mtime)
    response["Content-Length"] = statobj.st_size
    if encoding:
        response["Content-Encoding"] = encoding
    return response


@login_required
def files(request, template_name='core/files_upload.html'):
    return render_to_response(template_name,
                              RequestContext(request,
                                             {
                                              'full': True,
                                              }))

@login_required
def upload(request):
    if request.method == 'POST': # If the form has been submitted...
        rootpath = settings.FILES_ROOT
        if not os.path.exists(rootpath):
            os.makedirs(rootpath)

        f = request.FILES.get("files")
        wrapped_file = UploadedFile(f)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size
        
        fullpath = os.path.join(rootpath, f.name)
        if not os.path.exists(fullpath):
            destination = open(fullpath, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()

        #generating json response array
        result = []
        result.append({"name": filename, 
                       "size": file_size, 
                       "url": settings.FILES_URL + filename,
                       "delete_url": reverse("deletefile")+"?file="+filename, 
                       "delete_type":"GET",
                       })
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

def get_json_listfiles(request):
    files = os.listdir(settings.FILES_ROOT)
    files.remove("toupload")
    files.remove("todownload")
    result = []
    for f in files:
        result.append({"name": f, 
                       "size": os.path.getsize(os.path.join(settings.FILES_ROOT, f)), 
                       "url": settings.FILES_URL + f,
                       "delete_url": reverse("deletefile")+"?file="+f,
                       "delete_type":"GET",})
    response_data = simplejson.dumps(result)
    #checking for json data type
    #big thanks to Guy Shapiro
    if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
        mimetype = 'application/json'
    else:
        mimetype = 'text/plain'
    return HttpResponse(response_data, mimetype=mimetype)

def deletefile(request):
    thefile = request.GET.get("file")
    if thefile:
        try:
            os.remove(os.path.join(settings.FILES_ROOT, thefile))
        except:
            pass
    return HttpResponse(str(1))