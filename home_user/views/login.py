from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token

from common.utils import get_or_none

from home_user.models import User

class LoginView(APIView):

    permission_classes = [AllowAny,]

    def post(request : Request):
        # Retrieves User Credentials
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        # Authenticate
        user = get_or_none(User, username=username)

        # Fail for None or Bad Password
        if user is None or not user.check_password(password):
            return Response(
                data={
                    "success": "fail",
                    "message": "incorrect username and/or password"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create Token for Success
        token = Token.objects