import json
from datetime import datetime, timedelta

from django.db.models import Q, Count
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.posts.models import Post
from apps.posts.serializers import PostSerializer
from .models import Comment, Like, Blessing
from .serializers import CommentSerializer, LikeSerializer, BlessingSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author').all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        post_id = self.kwargs.get('post_id') or self.request.query_params.get('post_id')
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user, post_id=post_id)


class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.filter(id=post_id).first()
        if not post:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
            return Response({'liked': False, 'count': Like.objects.filter(post=post).count()})
        return Response({'liked': True, 'count': Like.objects.filter(post=post).count()})


class BlessingViewSet(viewsets.ModelViewSet):
    queryset = Blessing.objects.select_related('author').all()
    serializer_class = BlessingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        post_id = self.kwargs.get('post_id') or self.request.query_params.get('post_id')
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user, post_id=post_id)


class SearchView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        q = request.query_params.get('q', '')
        date_from = request.query_params.get('date_from', '')
        date_to = request.query_params.get('date_to', '')
        tags = request.query_params.get('tags', '')
        author = request.query_params.get('author', '')

        posts = Post.objects.prefetch_related('media', 'author').annotate(
            like_count=Count('likes', distinct=True),
            comment_count=Count('comments', distinct=True),
            blessing_count=Count('blessings', distinct=True),
        ).all()

        if q:
            posts = posts.filter(content__icontains=q)
        if date_from:
            posts = posts.filter(created_at__gte=date_from)
        if date_to:
            posts = posts.filter(created_at__lte=date_to)
        if tags:
            try:
                tag_list = json.loads(tags) if isinstance(tags, str) else tags
                for tag in tag_list:
                    posts = posts.filter(tags__contains=tag)
            except (json.JSONDecodeError, TypeError):
                pass
        if author:
            posts = posts.filter(author_id=author)

        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = PostSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            from rest_framework.pagination import PageNumberPagination
            self._paginator = PageNumberPagination()
            self._paginator.page_size = 20
        return self._paginator

    def paginate_queryset(self, queryset):
        return self.paginator.paginate_queryset(queryset, self.request)

    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data)


class OnThisDayView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        now = timezone.now()
        today = now.date()

        last_year = today - timedelta(days=365)
        last_month = today - timedelta(days=30)

        posts = Post.objects.prefetch_related('media', 'author').annotate(
            like_count=Count('likes', distinct=True),
            comment_count=Count('comments', distinct=True),
            blessing_count=Count('blessings', distinct=True),
        ).all()

        last_year_posts = posts.filter(
            created_at__month=last_year.month,
            created_at__day=last_year.day,
        )

        last_month_posts = posts.filter(
            created_at__month=last_month.month,
            created_at__day=last_month.day,
        )

        return Response({
            'last_year': PostSerializer(last_year_posts, many=True).data,
            'last_month': PostSerializer(last_month_posts, many=True).data,
        })
