from rest_framework import serializers

from .models import Comment, Like, Blessing
from apps.accounts.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']
        read_only_fields = ['id', 'post', 'author', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']
        read_only_fields = ['id', 'created_at']


class BlessingSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Blessing
        fields = ['id', 'post', 'author', 'content', 'created_at']
        read_only_fields = ['id', 'post', 'author', 'created_at']
