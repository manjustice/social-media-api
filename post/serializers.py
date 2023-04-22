from rest_framework import serializers
from .models import Post, Hashtag


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ("name", )


class PostSerializer(serializers.ModelSerializer):
    hashtags = HashtagSerializer(many=True, read_only=True)
    user = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
