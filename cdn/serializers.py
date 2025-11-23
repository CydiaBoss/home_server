from rest_framework import serializers
from cdn.models import Person, Share, Tag

class TagSerializer(serializers.ModelSerializer):
	is_person = serializers.SerializerMethodField()

	def get_is_person(self, obj : Tag):
		return Person.objects.filter(pk=obj.pk).exists()

	class Meta:
		model = Tag
		fields = ["id", "name", "created_by", "is_person"]

class ShareSerializer(serializers.ModelSerializer):
	class Meta:
		model = Share
		fields = ["id", "key", "media", "expires_at"]