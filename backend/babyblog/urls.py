from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.accounts.urls')),
    path('api/', include('apps.posts.urls')),
    path('api/', include('apps.social.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

from apps.spa_view import spa_index
urlpatterns += [
    re_path(r'^.*$', spa_index, name='spa-index'),
]
