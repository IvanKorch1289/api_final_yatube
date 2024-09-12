from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from posts.models import Comment, Group, Post
from api.permissions import IsAuthor
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)


User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthor)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthor]

    def get_post(self):
        return get_object_or_404(
            Post.objects.all(),
            id=self.kwargs.get('post_id')
        )

    def get_queryset(self):
        return Comment.objects.filter(post=self.get_post())

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_user(self, username):
        return get_object_or_404(User.objects.all(), username=username)

    def get_queryset(self):
        return self.request.user.subscribers.all()

    def create(self, request, *args, **kwargs):
        if 'following' not in request.data:
            return Response(status=HTTP_400_BAD_REQUEST)

        following = self.get_user(request.data['following'])

        if self.get_queryset().filter(following=following).exists():
            return Response(status=HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            following=self.get_user(serializer.initial_data['following'])
        )
