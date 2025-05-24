from django.core.paginator import Paginator
from django.db.models import Q
from django.http import FileResponse, Http404, HttpResponseNotModified
from django.utils.http import http_date
from django.utils.translation import gettext as _
from django.views import View
from django.views.static import was_modified_since

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from cdn.serializers import TagSerializer
from common.utils import get_filepath, get_or_none

from cdn.models import File, Person, Tag

class TagsView(APIView):
    
    # GET Tag
    def get(self, request : Request):
        """
        Get list of tags

        Route: [GET] /cdn/tag

        Query Parameters:
        - q: str = "" (Search query for the tag)
        - created_by: int : user_id = -1 (Filter by the user who made it)
        - people: bool = 0 (Filter for people tags only)
        """
        # Parse queries
        query = request.query_params.get("q", "")
        created_by = request.query_params.get("created_by", "-1")
        people = request.query_params.get("people", "0") == "1"

        # Make Query
        filters = Q(name__icontains=query)

        # Created by check
        if created_by != "-1":
            filters &= Q(created_by__id=created_by)

        # Query Based on Model
        if people:
            tags = Person.objects.filter(filters)
        else:
            tags = Tag.objects.filter(filters)

        # Serialize and Return
        tag_data = TagSerializer(tags, many=True)

        return Response({
            "status": "success",
            "payload": tag_data.data
        })
    
    # POST Tag
    def post(self, request : Request):
        """
        Make a tag

        Route: [POST] /cdn/tag

        # Request Body
        - name: str (Name for tag)
        - person: bool (If this is a person)
        - thumbnail: int (Id of photo for thumbnail; only used if 'person' is set to true)
        """
        # Parse body
        name = request.data.get("name")
        person = request.data.get("person", False)
        thumbnail = request.data.get("thumbnail")

        # Make Query
        if get_or_none(Tag, name=name) is not None:
            return Response({
                "status": "fail",
                "message": "tag with that name already exists"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check for Personhood
        if person:
            obj = Person(
                name=name,
            )

            # Thumbnail Add
            if thumbnail is not None:
                obj.thumbnail_id = thumbnail
        
        else:
            obj = Tag(
                name=name
            )

        # Save
        obj.created_by = request.user
        obj.save()

        return Response({
            "status": "success",
            "message": "tag made successfully",
            "payload": obj.pk
        })
    
class TagsModifyView(APIView):
    
    # GET Tag
    def put(self, request : Request, tag_id=""):
        """
        Update a tag's info

        Route: [PUT] /cdn/tag/:tag_id

        # Request Path
        - tag_id: ID of tag to update

        # Request Body
        - name: str (new name for tag)
        - thumbnail: int (ID of File for thumbnail; only works for Person tags)
        """
        # Parse body
        name = request.data.get("name")
        thumbnail = request.query_params.get("thumbnail")

        if name is None and thumbnail is None:
            return Response({
                "status": "fail",
                "message": "nothing to update"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Try finding objects
        tag = get_or_none(Person, id=tag_id)

        # Add thumbnail if possible
        if tag is not None:
            tag.thumbnail_id = thumbnail

        # Get Actual Tag otherwise
        else:
            tag = get_or_none(Tag, id=tag_id)

        # Fail if still none
        if tag is None:
            return Response({
                "status": "fail",
                "message": "tag does not exist"
            }, status=status.HTTP_404_NOT_FOUND)

        # Update name
        tag.name = name
        tag.save()

        return Response({
            "status": "success",
            "message": "tag updated"
        })
    
    # POST Tag
    def delete(self, request : Request, tag_id=""):
        """
        Delete a tag

        Route: [DELETE] /cdn/tag/:tag_id

        # Request Path
        - tag_id: ID of tag to remove
        """
        # Make Query
        tag = get_or_none(Tag, id=tag_id)
        if tag is None:
            return Response({
                "status": "fail",
                "message": "tag does not exist"
            }, status=status.HTTP_404_NOT_FOUND)

        # Save
        tag.delete()

        return Response({
            "status": "success",
            "message": "tag deleted successfully",
        })