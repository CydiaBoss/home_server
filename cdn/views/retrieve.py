import mimetypes, random

from django.http.request import HttpRequest
from django.http import FileResponse, Http404, HttpResponseNotModified
from django.utils.http import http_date
from django.utils.translation import gettext as _
from django.views import View
from django.views.static import was_modified_since

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from common.utils import get_filepath

from cdn.models import File

class MediaRetrieveView(View):
    
    # GET Media
    def get(self, request : HttpRequest, path=""):
        '''
        Retrieve a media file

        # Template from Django serve function #

        Route: [GET] /cdn/media/:path_to_file
        '''
        # Get Path
        filepath = get_filepath(path=path)

        # Fail Directory or Not Found
        if filepath.is_dir() or not filepath.exists():
            raise Http404(_(f"“{filepath}” is not accessible"))
        
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
    
class MediaRetrieveListView(APIView):
    
    # GET Media
    def get(self, request : Request):
        '''
        Retrieve a list of media files

        Route: [GET] /cdn/list

        Query Parameters:
        - random: bool = False (Randomize the list)
        - total_amt: int = 50 (Total amount of images to retrieve; ignored if ids or names are provided)
        - ids: list = [] (List of images to retrieve using ids; ignored if random is True)
        - names: list = [] (List of images to retrieve using names; ignored if random is True)
        '''
        # Get Query Parameters
        randomize = request.query_params.get("random", False) == "true"
        total_amt = int(request.query_params.get("total_amt", 50))
        ids = request.query_params.get("ids", [])
        if type(ids) == str:
            ids = ids.split(",")
        names = request.query_params.get("names", [])
        if type(names) == str:
            names = names.split(",")

        # Get Files randomily
        if randomize:
            # Generate random list of ids
            ids = list(File.objects.values_list("id", flat=True))
            random.shuffle(ids)
            ids = ids[:total_amt]

            # Get Files
            files = File.objects.filter(id__in=ids)

            # Generate Response
            payload = {
                "status": "success",
                "total": len(files),
                "files": []
            }

            # Return Response
            for file in files:
                payload["files"].append({
                    "id": file.id,
                    "name": file.file_name,
                    "ext": file.file_ext,
                    "full_name": f"{file.file_name}.{file.file_ext}",
                    "url": file.path
                })

            # Return Response
            return Response(payload)
        
        # Get Files by ids
        elif len(ids) > 0:
            # Get Files
            files = File.objects.filter(id__in=ids)

            # Generate Response
            payload = {
                "status": "success",
                "total": len(files),
                "files": []
            }

            # Return Response
            for file in files:
                payload["files"].append({
                    "id": file.id,
                    "name": file.file_name,
                    "ext": file.file_ext,
                    "full_name": f"{file.file_name}.{file.file_ext}",
                    "url": file.path
                })

            # Return Response
            return Response(payload)
        
        # Get Files by names
        elif len(names) > 0:
            # Get Files
            files = File.objects.filter(file_name__in=names)

            # Generate Response
            payload = {
                "status": "success",
                "total": len(files),
                "files": []
            }

            # Return Response
            for file in files:
                payload["files"].append({
                    "id": file.id,
                    "name": file.file_name,
                    "ext": file.file_ext,
                    "full_name": f"{file.file_name}.{file.file_ext}",
                    "url": file.path
                })

            # Return Response
            return Response(payload)
        
        else:
            return Response({
                "status": "fail",
                "error": "No valid query parameters provided"
            }, status=status.HTTP_400_BAD_REQUEST)