from rest_framework import serializers
from home_user.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		exclude = ["password",]