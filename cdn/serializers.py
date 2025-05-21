from rest_framework import serializers
from cdn.models import Tag

class TagSerializer(serializers.ModelSerializer):
	is_person = serializers.BooleanField(write_only=True)

	class Meta:
		model = Tag
		fields = ["id", "name", "created_by"]