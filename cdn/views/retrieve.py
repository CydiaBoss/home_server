import mimetypes

from django.http.request import HttpRequest
from django.http import FileResponse, Http404, HttpResponseNotModified
from django.utils.http import http_date
from django.utils.translation import gettext as _
from django.views import View
from django.views.static import was_modified_since

from common.utils import get_filepath

class MediaRetrieveView(View):
    
    # GET Media
    def get(self, request : HttpRequest, path=""):
        '''
        Retrieve a media file

        # Template from Django serve function #

        Route: [GET] /cdn/media/:path_to_file/
        '''
        # Get Path
        filepath = get_filepath(path=path)

        # Fail Directory or Not Found
        if filepath.is_dir() or not filepath.exists():
            raise Http404(_("“%(path)s” is not accessible") % {"path": filepath})
        
        # Respect the If-Modified-Since header.
        statobj = filepath.stat()
        if not was_modified_since(
            request.META.get("HTTP_IF_MODIFIED_SINCE"), statobj.st_mtime
        ):
            return HttpResponseNotModified()
        
        # Generate Static View
        content_type, encoding = mimetypes.guess_type(str(filepath))
        content_type = content_type or "application/octet-stream"
        response = FileResponse(filepath.open("rb"), content_type=content_type)
        response.headers["Last-Modified"] = http_date(statobj.st_mtime)
        if encoding:
            response.headers["Content-Encoding"] = encoding
        return response