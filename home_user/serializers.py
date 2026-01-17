from typing import Union
from rest_framework import serializers
from home_user.models import User, UserSetting

class UserSettingSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserSetting
		exclude = ["id", "user"]

class UserSerializer(serializers.ModelSerializer):

	full_name = serializers.SerializerMethodField()
	avatar = serializers.SerializerMethodField()
	settings = UserSettingSerializer(read_only=True)

	def get_full_name(self, obj : User) -> str:
		return obj.full_name
	
	def get_avatar(self, obj : User) -> Union[str, None]:
		if obj.avatar.count() == 0:
			return None
		else:
			return obj.avatar.first().thumbnail.path

	class Meta:
		model = User
		exclude = ["password", "groups", "user_permissions", "is_superuser"]