from rest_framework import serializers
from home_user.models import User, UserSetting

class UserSettingSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserSetting
		exclude = ["id", "user"]

class UserSerializer(serializers.ModelSerializer):

	settings = UserSettingSerializer(read_only=True)

	class Meta:
		model = User
		exclude = ["password", "groups", "user_permissions", "is_superuser"]