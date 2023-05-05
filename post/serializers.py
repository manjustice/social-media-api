from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "created_at", "content", "author", "hashtags")
        read_only_fields = ("id", "author")


class PostListSerializer(PostSerializer):
    hashtags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
