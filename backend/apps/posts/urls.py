from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'media', views.MediaViewSet, basename='media')
router.register(r'milestones', views.MilestoneViewSet, basename='milestone')

urlpatterns = [
    path('upload/', views.MediaUploadView.as_view(), name='media-upload'),
    path('', include(router.urls)),
]
