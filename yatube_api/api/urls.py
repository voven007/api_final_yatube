from django.urls import path, include
from api.views import PostViewSet, FollowViewSet, GroupViewSet, CommentViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'follow', FollowViewSet, basename='follow')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(
    r'^posts/(?P<post_id>\d+)/comments',
    CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
