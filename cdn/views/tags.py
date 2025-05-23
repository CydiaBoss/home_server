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
        # Parse queries
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
        obj.save()

        return Response({
            "status": "success",
            "message": f"tag '{name}' made successfully",
            "payload": obj.pk
        })