from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Comment, Post
from .serializers import CommentSerializer, PostSerializer


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method == "PATCH" and obj.author == request.user:
            return True
        return obj.author == request.user

    # if request.method in permissions.SAFE_METHODS:
    #     return True
    #
    #     # Instance must have an attribute named `owner`.
    # return obj.owner == request.user


@api_view(['GET', 'POST'])
def api_comments(request, pk):
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    comments = Comment.objects.filter(post__id=pk)
    print(comments)
    serializer = CommentSerializer(comments, many=True)
    print(serializer)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_comments_detail(request, pk, pk2):
    one_comment = Comment.objects.filter(post__id=pk).get(pk=pk2)
    print(one_comment)
    if request.method == 'PUT':
        serializer = CommentSerializer(
            one_comment,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if one_comment.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        one_comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PATCH':
        serializer = CommentSerializer(
            one_comment,
            data=request.data,
            partial=True
        )
        if one_comment.author == request.user:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_403_FORBIDDEN)
    serializer = CommentSerializer(one_comment)
    return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def get_permissions(self):
    #     if self.request.method == "GET":
    #         return (permissions.AllowAny(),)
    #     # if self.request.method == "PATCH" and post.author != request.user:
    #     #     return Response(status=status.HTTP_403_FORBIDDEN)
    #     return super().get_permissions()
