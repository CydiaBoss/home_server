import mimetypes, random

from django.core.paginator import Paginator
from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from cdn.serializers import CommentSerializer

from cdn.models import Comment
    
class MediaDetailView(APIView):
    
    # GET Media
    def get(self, request : Request, media_id=""):
        '''
        Retrieve details about a media
        This means comments, etc.

        Route: [GET] /cdn/detail/:media_id

        Query Parameters:
        - total_amt: int = 50 (Total amount of comments to retrieve per page)
        - page: int = 1 (Current page to retrieve of the query)
        '''
        # Error if nothing
        if (media_id == ""):
            return Response({
                "status": "fail",
                "message": "No media ID provided"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get Query Parameters
        total_amt = int(request.query_params.get("total_amt", 50))
        page = int(request.query_params.get("page", 1))

        # Make Paginator
        paginator = Paginator(Comment.objects.filter(media__id=media_id), total_amt)
        page_obj = paginator.get_page(page)

        # Generate Response
        payload = {
            "status": "success",
            "total": (page_obj.end_index() + 1) - page_obj.start_index(),
            "page_count": paginator.num_pages,
            "prev_page": page_obj.previous_page_number() if page_obj.has_previous() else -1,
            "next_page": page_obj.next_page_number() if page_obj.has_next() else -1,
            "payload": CommentSerializer(page_obj, many=True).data
        }

        # Return Response
        return Response(payload)