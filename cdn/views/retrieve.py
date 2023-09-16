import mimetypes
import posixpath
from pathlib import Path

from django.conf import settings
from django.http.request import HttpRequest
from django.http import FileResponse, Http404, HttpResponseNotModified
from django.utils._os import safe_join
from django.utils.http import http_date
from django.utils.translation import gettext as _
from django.views import View
from django.views.static import was_modified_since

class MediaRetrieveView(View):
    
    # GET Media
    def get(self, request : HttpRequest, path=""):
        '''
        Retrieve a media file

        # Template from Django serve function #

        Route: [GET] /cdn/media/:path_to_file/
        '''
        # Get Path
        path = posixpath.normpath(path).lstrip("/")
        fullpath = Path(safe_join(settings.MEDIA_ROOT, path))

        # Fail Directory or Not Found
        if fullpath.is_dir() or not fullpath.exists():
            raise Http404(_("“%(path)s” is not accessible") % {"path": fullpath})
        
        # Respect the If-Modified-Since header.
        statobj = fullpath.stat()
        if not was_modified_since(
            request.META.get("HTTP_IF_MODIFIED_SINCE"), statobj.st_mtime
        ):
            return HttpResponseNotModified()
        
        # Generate Static View
        content_type, encoding = mimetypes.guess_type(str(fullpath))
        content_type = content_type or "application/octet-stream"
        response = FileResponse(fullpath.open("rb"), content_type=content_type)
        response.headers["Last-Modified"] = http_date(statobj.st_mtime)
        if encoding:
            response.headers["Content-Encoding"] = encoding
        return response