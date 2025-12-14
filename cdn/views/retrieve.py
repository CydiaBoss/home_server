import mimetypes, random

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import FileResponse, HttpResponseNotModified
from django.utils.http import http_date
from django.utils.translation import gettext as _
from django.views.static import was_modified_since

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from cdn.serializers import DetailedFileSerializer, FileSerializer
from common.utils import get_filepath

from cdn.models import File

class MediaRetrieveView(APIView):
    
    # GET Media
    def get(self, request : Request, path=""):
        '''
        Retrieve a media file

        # Template from Django serve function #

        Route: [GET] /cdn/media/:path_to_file
        '''
        # Get Path
        filepath = get_filepath(path=path)

        # Fail Directory or Not Found
        if filepath.is_dir() or not filepath.exists():
            return Response({
                "status": "fail",
                "message": f'"{filepath}" does not exist'
            }, status=status.HTTP_404_NOT_FOUND)
        
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
        - detailed: bool = 0 (Whether to use detailed view)
        - random: bool = 0 (Randomize the list)
        - personal: bool = 0 (Only get auth user's files)
        - total_amt: int = 50 (Total amount of images to retrieve per page; total amount to query if used with random)
        - page: int = 1 (Current page to retrieve of the query)
        - ids: list = [] (List of images to retrieve using ids; ignored if random is True)
        - names: list = [] (List of images to retrieve using names; ignored if random is True)
        - q: str = "" (Query using a search string; ignored if one of the previous methods are used)
        '''
        # Get Query Parameters
        detailed = request.query_params.get("detailed", "0") == "1"
        randomize = request.query_params.get("random", "0") == "1"
        personal = request.query_params.get("personal", "0") == "1"
        query = request.query_params.get("q", "")
        total_amt = int(request.query_params.get("total_amt", 50))
        page = int(request.query_params.get("page", 1))
        ids = request.query_params.get("ids", [])
        if type(ids) == str:
            ids = ids.split(",")
        names = request.query_params.get("names", [])
        if type(names) == str:
            names = names.split(",")

        # Personal filter
        personal_filter = Q(uploaded_by=request.user) if personal else Q()

        # Get Files randomly
        if randomize:
            # TODO fix this as will be very bad when a lot of data
            # Generate random list of ids
            ids = list(File.objects.filter(personal_filter).values_list("id", flat=True))
            random.shuffle(ids)
            ids = ids[:total_amt]

            # Get Files
            files = File.objects.filter(id__in=ids)
        
        # Get Files by ids
        elif len(ids) > 0:
            # Get Files
            files = File.objects.filter(personal_filter, id__in=ids)
        
        # Get Files by names
        elif len(names) > 0:
            # Get Files
            files = File.objects.filter(personal_filter, file_name__in=names)

        # Query string method
        elif query != "":
            # Get Files
            files = File.objects.filter(personal_filter, Q(file_name__icontains=query) | Q(file_ext__icontains=query))
        
        else:
            return Response({
                "status": "fail",
                "message": "No valid query parameters provided"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Make Paginator
        paginator = Paginator(files, total_amt)
        page_obj = paginator.get_page(page)

        # Generate Response
        payload = {
            "status": "success",
            "total": (page_obj.end_index() + 1) - page_obj.start_index(),
            "page_count": paginator.num_pages,
            "prev_page": page_obj.previous_page_number() if page_obj.has_previous() else -1,
            "next_page": page_obj.next_page_number() if page_obj.has_next() else -1,
            "payload": DetailedFileSerializer(page_obj, many=True).data if detailed else FileSerializer(page_obj, many=True).data
        }

        # Return Response
        return Response(payload)