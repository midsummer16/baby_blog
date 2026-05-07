import json
import os

from rest_framework import serializers

from .models import Post, Media, Milestone
from apps.accounts.serializers import UserSerializer


class MediaSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)

    class Meta:
        model = Media
        fields = ['id', 'file', 'media_type', 'thumbnail', 'uploaded_at', 'uploaded_by']
        read_only_fields = ['id', 'uploaded_at', 'uploaded_by']


class TagField(serializers.Field):
    def to_representation(self, value):
        try:
            return json.loads(value) if isinstance(value, str) else value
        except (json.JSONDecodeError, TypeError):
            return []

    def to_internal_value(self, data):
        if isinstance(data, str):
            return data
        return json.dumps(data, ensure_ascii=False)


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    media = MediaSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(read_only=True, default=0)
    comment_count = serializers.IntegerField(read_only=True, default=0)
    blessing_count = serializers.IntegerField(read_only=True, default=0)
    is_liked = serializers.SerializerMethodField()
    tags = TagField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'tags', 'media', 'created_at', 'updated_at',
                  'like_count', 'comment_count', 'blessing_count', 'is_liked']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    media_ids = serializers.ListField(child=serializers.IntegerField(), required=False, default=list)
    milestone_type = serializers.ChoiceField(
        choices=Milestone.MILESTONE_TYPES, required=False, allow_null=True, default=None
    )
    milestone_date = serializers.DateField(required=False, allow_null=True, default=None)
    tags = TagField(required=False, default='[]')

    class Meta:
        model = Post
        fields = ['content', 'tags', 'media_ids', 'milestone_type', 'milestone_date']

    def create(self, validated_data):
        media_ids = validated_data.pop('media_ids', [])
        milestone_type = validated_data.pop('milestone_type', None)
        milestone_date = validated_data.pop('milestone_date', None)
        validated_data['author'] = self.context['request'].user
        post = Post.objects.create(**validated_data)
        if media_ids:
            Media.objects.filter(id__in=media_ids, post__isnull=True).update(post=post)
        if milestone_type and milestone_date:
            Milestone.objects.get_or_create(
                baby=post.author,
                milestone_type=milestone_type,
                achieved_date=milestone_date,
                defaults={'post': post, 'description': ''},
            )
        return post


class MediaUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'file', 'media_type', 'thumbnail', 'uploaded_at']
        read_only_fields = ['id', 'media_type', 'thumbnail', 'uploaded_at']

    def validate_file(self, value):
        ext = os.path.splitext(value.name)[1].lower()
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.mp4', '.webm']
        if ext not in allowed_extensions:
            raise serializers.ValidationError(f'Unsupported file extension: {ext}')
        if ext in ['.mp4', '.webm']:
            max_size = 200 * 1024 * 1024
        else:
            max_size = 20 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError(f'File size must not exceed {max_size // (1024*1024)}MB.')
        return value

    def create(self, validated_data):
        ext = os.path.splitext(validated_data['file'].name)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png']:
            validated_data['media_type'] = 'image'
        elif ext in ['.mp4', '.webm']:
            validated_data['media_type'] = 'video'
        validated_data['uploaded_by'] = self.context['request'].user
        return super().create(validated_data)


class MilestoneSerializer(serializers.ModelSerializer):
    baby = UserSerializer(read_only=True)
    milestone_type_display = serializers.SerializerMethodField()

    class Meta:
        model = Milestone
        fields = [
            'id', 'baby', 'milestone_type', 'milestone_type_display',
            'achieved_date', 'description', 'post', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_milestone_type_display(self, obj):
        return obj.get_milestone_type_display()

    def create(self, validated_data):
        milestone, _ = Milestone.objects.get_or_create(
            baby=validated_data['baby'],
            milestone_type=validated_data['milestone_type'],
            achieved_date=validated_data['achieved_date'],
            defaults=validated_data,
        )
        return milestone
