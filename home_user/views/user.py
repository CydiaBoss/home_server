from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from common.utils import get_or_none

from home_user.models import User
from home_user.serializers import UserSerializer

class UserView(APIView):

	def get(self, request : Request):
		"""
		Grabs request user's data
		"""
		return Response({
			"success": "success",
			"payload": UserSerializer(request.user).data
		})