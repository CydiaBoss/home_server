from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

class MediaView(APIView):

    def get(self, request : Request):

        return Response({"success" : "ok"})