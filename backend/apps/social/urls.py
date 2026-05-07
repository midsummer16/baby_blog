from django.urls import path

from . import views

urlpatterns = [
    path('posts/<int:post_id>/like/', views.LikeView.as_view(), name='post-like'),
    path('posts/<int:post_id>/comments/', views.CommentViewSet.as_view({
        'get': 'list', 'post': 'create',
    }), name='post-comments'),
    path('comments/<int:pk>/', views.CommentViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy',
    }), name='comment-detail'),
    path('posts/<int:post_id>/blessings/', views.BlessingViewSet.as_view({
        'get': 'list', 'post': 'create',
    }), name='post-blessings'),
    path('blessings/<int:pk>/', views.BlessingViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy',
    }), name='blessing-detail'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('on-this-day/', views.OnThisDayView.as_view(), name='on-this-day'),
]
