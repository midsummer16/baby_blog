import os

from django.db.models import Count
from rest_framework import viewsets, generics, permissions, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Media, Milestone
from .serializers import (
    PostSerializer, PostCreateSerializer, MediaSerializer,
    MediaUploadSerializer, MilestoneSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.prefetch_related('media', 'author').all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer

    def get_queryset(self):
        qs = Post.objects.prefetch_related('media', 'author').all()
        qs = qs.annotate(
            like_count=Count('likes', distinct=True),
            comment_count=Count('comments', distinct=True),
            blessing_count=Count('blessings', distinct=True),
        )
        qs = qs.order_by('-created_at')
        author = self.request.query_params.get('author')
        if author:
            qs = qs.filter(author_id=author)
        return qs

    def perform_create(self, serializer):
        serializer.save()


class MediaUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request):
        serializer = MediaUploadSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        media = serializer.save()
        return Response(MediaSerializer(media).data, status=status.HTTP_201_CREATED)


class MediaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [permissions.AllowAny]


class MilestoneViewSet(viewsets.ModelViewSet):
    queryset = Milestone.objects.select_related('baby', 'post').all()
    serializer_class = MilestoneSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(baby=self.request.user)

    @action(detail=False, methods=['get'], url_path='timeline')
    def timeline(self, request):
        qs = self.get_queryset()
        milestones_by_month = {}
        for m in qs:
            key = m.achieved_date.strftime('%Y-%m')
            if key not in milestones_by_month:
                milestones_by_month[key] = {
                    'month': key,
                    'milestones': [],
                }
            milestones_by_month[key]['milestones'].append(
                MilestoneSerializer(m).data
            )
        result = sorted(milestones_by_month.values(), key=lambda x: x['month'], reverse=True)
        return Response(result)
