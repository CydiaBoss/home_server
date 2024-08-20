from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token

from common.utils import get_or_none

from home_user.models import User

class LogoutView(APIView):

    permission_classes = [AllowAny,]

    def get(self, request : Request):
        # Retrieves username
        username = request.query_params.get("username", None)

        # Look for user
        user = get_or_none(User, username=username)

        # Fail for None 
        if user is None:
            return Response(
                data={
                    "success": "fail",
                    "message": "user not found"
                }, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Create Token for Success or Retrieve existing
        token = get_or_none(Token, user=user)
        if token is not None:
            token.delete()

        # Return
        return Response(
            data={
                "success": "ok",
                "message": "user logged out"
            }, 
            status=status.HTTP_200_OK
        )