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
from common.utils import get_filepath

from cdn.models import File, Person, Tag

class TagsView(APIView):
    
    # GET Media
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
        filters = Q()

        # Add Query if not blank
        if query != "":
            filters = Q(name__icontains=query)

        # Created by check
        if created_by != "-1":
            filters &= Q(created_by__id=created_by)

        print(filters)

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