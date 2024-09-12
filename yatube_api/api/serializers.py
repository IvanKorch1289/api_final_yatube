from django.contrib.auth import get_user_model

from rest_framework import serializers

from posts.models import Comment, Follow, Group, Post


User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор объекта поста."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')
        read_only_fields = ('id', 'pub_date')
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор объектов групп."""

    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор объектов комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True,slug_field='username'
    )

    class Meta:
        fields = ('id', 'post', 'author', 'text', 'created')
        read_only_fields = ('created', 'post')
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор объекта подписки."""

    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        required=True
    )

    class Meta:
        fields = ('user', 'following',)
        model = Follow

    def validate_following(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError(
                'Запрещено в following передавать собственную учетную запись'
            )
