from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token

from common.utils import get_or_none

from home_user.models import User

class UploadView(APIView):

    def post(self, request : Request):
        '''
        Upload API for manual user upload

        Route: [GET] /cdn/upload/
        '''
        # Retrieves username
        username = request.user

        # TODO file upload logic

        # Return
        return Response(
            data={
                "success": "ok",
                "message": "user logged out"
            }, 
            status=status.HTTP_200_OK
        )