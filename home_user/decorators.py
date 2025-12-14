from typing import Any, Callable
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

def staff_only(func : Callable[[Request, Any], Response]):
	"""
	Enforce staff user only check
	"""
	def wrapper(request : Request, *args, **kwargs):
		# Check user status
		if (request.user == None or not request.user.is_active):
			return Response({
				"success": "fail",
				"message": "no active auth user found"
			}, status=status.HTTP_404_NOT_FOUND)
		
		# Check user perms
		if (not request.user.is_staff):
			return Response({
				"success": "fail",
				"message": "user not a staff"
			}, status=status.HTTP_403_FORBIDDEN)
		
		# Execute
		return func(request, *args, **kwargs)
	return wrapper