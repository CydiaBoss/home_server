from rest_framework import serializers
from cdn.models import Comment, File, Person, Share, Tag, VideoDetail

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

class VideoDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = VideoDetail
		fields = ["timestamp",]

class FileSerializer(serializers.ModelSerializer):
	class Meta:
		model = File
		fields = ["id", "path", "full_name"]

class DetailedFileSerializer(FileSerializer):
	video_detail = VideoDetailSerializer(read_only=True)
	comment_count = serializers.SerializerMethodField()
	like_count = serializers.SerializerMethodField()

	def get_comment_count(self, obj : File):
		return obj.comments.count()

	def get_like_count(self, obj : File):
		return obj.liked_by.count()

	class Meta:
		model = File
		fields = ["id", "path", "full_name", "title", "description", "tags", "uploaded_by", "video_detail", "comment_count", "like_count"]

class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ["id", "written_by", "comment"]