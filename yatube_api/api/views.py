from django.shortcuts import get_object_or_404
from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer
from .serializers import CommentSerializer, FollowSerializer

from .permissions import IsAuthorOrReadOnely
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnely,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthorOrReadOnely,)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnely,)

    def get_post(self):
        return get_object_or_404(
            Post,
            id=self.kwargs.get('post_id')
        )

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            post=self.get_post()
        )

    def get_queryset(self):
        return self.get_post().comments.all()


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username', )

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return user.follower.all()
