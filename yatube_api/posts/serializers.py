from rest_framework import serializers

from .models import Comment, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'pub_date')
        read_only_fields = ('author',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
