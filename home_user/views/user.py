from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from common.utils import get_or_none

from home_user.decorators import staff_only
from home_user.models import User, UserSetting
from home_user.serializers import UserSerializer

class UserView(APIView):

	def get(self, request : Request):
		"""
		Grabs request user's data

        Route: [GET] /user/data
		"""
		return Response({
			"success": "success",
			"payload": UserSerializer(request.user).data
		})
	
	@staff_only
	def post(self, request : Request):
		"""
		Create a new user
		Only for staff users

        Route: [POST] /user/data

        # Request Body
        - first_name: str (first name)
        - last_name: str (last name)
		- bio: str (biography)
		- username: str (username)
        - email: str (email address)
		- password: str (password)
		- is_staff: bool (is admin user?)
		"""
		username = request.data.get("username")
		if get_or_none(User, username=username) is not None:
			return Response({
				"success": "fail",
				"message": "username already used"
			}, status=status.HTTP_400_BAD_REQUEST)
		
		email = request.data.get("email")
		if get_or_none(User, email=email) is not None:
			return Response({
				"success": "fail",
				"message": "email address already used"
			}, status=status.HTTP_400_BAD_REQUEST)
		
		# Create new user
		new_user = User(
			username=username,
			email=email,
			first_name=request.data.get("first_name", ""),
			last_name=request.data.get("last_name", ""),
			bio=request.data.get("bio", "")
		)

		# Set password
		new_user.set_password(request.data.get("password"))

		# Role
		new_user.is_staff = request.data.get("is_staff", "false") == "true"

		# Save
		try:
			new_user.save()

			return Response({
				"success": "success",
				"message": "user created"
			})
		except:
			return Response({
				"success": "fail",
				"message": "user could not be created"
			}, status=status.HTTP_400_BAD_REQUEST)
	
	def put(self, request : Request):
		"""
		Modify personal user details

        Route: [PUT] /user/data

        # Request Body
		- email: str (email address)
        - first_name: str (first name)
        - last_name: str (last name)
		- bio: str (biography)
		- password: str (password)
		- dark_mode: bool (uses dark mode)
		- lang: str (language to use)
		"""
		# Update Email
		if "email" in request.data: 
			temp_email = request.data.get("email", request.user.email)
			if request.user.email != temp_email and get_or_none(User, email=temp_email) is not None:
				return Response({
					"success": "fail",
					"message": "email address already used"
				}, status=status.HTTP_400_BAD_REQUEST)
			else:
				request.user.email = temp_email
		
		# Update Names
		temp_first_name = request.data.get("first_name", request.user.first_name)
		if request.user.first_name != temp_first_name:
			request.user.first_name = temp_first_name
		temp_last_name = request.data.get("last_name", request.user.last_name)
		if request.user.last_name != temp_last_name:
			request.user.last_name = temp_last_name

		# Update Bio
		temp_bio = request.data.get("bio", request.user.bio)
		if request.user.bio != temp_bio:
			request.user.bio = temp_bio

		# Update user settings
		if "dark_mode" in request.data or "lang" in request.data:
			# Make UserSettings if not already
			user_settings : UserSetting = request.user.settings
			if user_settings is None:
				user_settings = UserSetting()
				user_settings.user = request.user

			user_settings.dark_mode = request.data.get("dark_mode", user_settings.dark_mode)
			user_settings.lang = request.data.get("lang", user_settings.lang)
			user_settings.save()

		# Update Password
		if "password" in request.data:
			request.user.set_password(request.data.get("password"))

		request.user.save()

		return Response({
			"success": "success",
			"message": "user updated"
		})