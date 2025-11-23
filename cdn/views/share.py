from datetime import datetime
import mimetypes, random

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import FileResponse, HttpResponseNotModified
from django.utils.http import http_date
from django.utils.translation import gettext as _
from django.views.static import was_modified_since

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request

from cdn.serializers import ShareSerializer
from common.utils import get_filepath, get_or_none

from cdn.models import File, Share

class MediaShareView(APIView):
    
    permission_classes = [AllowAny,]
    
    # GET Media
    def get(self, request : Request, key=""):
        '''
        Retrieve a media file

        # Template from Django serve function #

        Route: [GET] /cdn/share/:key
        '''
        # Clean up key if needed
        key = key.removesuffix("/")

        # Get Key
        share_obj = get_or_none(Share, key=key)
        if share_obj == None:
            return Response({
                "status": "fail",
                "message": "share key does not exist"
            }, status=status.HTTP_404_NOT_FOUND)

        # Get Path
        filepath = get_filepath(path=share_obj.media.path)
        
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
    
class ShareView(APIView):
    
    # GET Tag
    def get(self, request : Request):
        """
        Get list of sharelink

        Route: [GET] /cdn/sharelink

        Query Parameters:
        - q: str = "" (Search query for the tag)
        """
        # Parse queries
        query = request.query_params.get("q", "")

        # Make Query
        filters = Q(name__icontains=query)

        # Get List
        sharelinks = Share.objects.filter(filters)

        # Serialize and Return
        sharelink_data = ShareSerializer(sharelinks, many=True)

        return Response({
            "status": "success",
            "payload": sharelink_data.data
        })
    
    # POST Tag
    def post(self, request : Request):
        """
        Make a sharelink

        Route: [POST] /cdn/sharelink

        # Request Body
        - media: int (media id to share)
        - expiry: int (unix time of expiry)
        """
        # Parse body
        media_id = request.data.get("media")
        expiry = request.data.get("expiry")
        
        # Make sharelink
        obj = Share(
            media__id=media_id,
            expires_at = datetime.fromtimestamp(float(expiry))
        )

        # Save
        obj.shared_by = request.user
        obj.save()

        return Response({
            "status": "success",
            "message": "sharelink made successfully",
            "payload": obj.key
        })
    
class ShareModifyView(APIView):
    
    # GET Tag
    def put(self, request : Request, share_id=""):
        """
        Update a tag's info

        Route: [PUT] /cdn/sharelink/:share_id

        # Request Path
        - share_id: ID of sharelink to update

        # Request Body
        - media: int (new media to use)
        - expiry: int (active link until)
        """
        # Parse body
        media = request.data.get("media")
        expiry = request.data.get("expiry")

        if media is None and expiry is None:
            return Response({
                "status": "fail",
                "message": "nothing to update"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Try finding objects
        share = get_or_none(Share, id=share_id)

        # Fail if no share
        if share is None:
            return Response({
                "status": "fail",
                "message": "sharelink not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # Update media
        if media is not None:
            new_media = get_or_none(File, id=media)
            if new_media is None:
                return Response({
                    "status": "fail",
                    "message": "media not found"
                }, status=status.HTTP_404_NOT_FOUND)
            share.media = new_media

        # Update expiration
        if expiry is not None:
            share.expires_at = datetime.fromtimestamp(float(expiry))

        # Success
        share.save()
        return Response({
            "status": "success",
            "message": "sharelink updated updated"
        })
    
    # POST Tag
    def delete(self, request : Request, share_id=""):
        """
        Delete a sharelink

        Route: [DELETE] /cdn/sharelink/:share_id

        # Request Path
        - share_id: ID of sharelink to remove
        """
        # Make Query
        tag = get_or_none(Share, id=share_id)
        if tag is None:
            return Response({
                "status": "fail",
                "message": "sharelink does not exist"
            }, status=status.HTTP_404_NOT_FOUND)

        # Save
        tag.delete()

        return Response({
            "status": "success",
            "message": "sharelink deleted successfully",
        })