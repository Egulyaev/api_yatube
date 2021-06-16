from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        if request.method == "PATCH" and obj.author == request.user:
            return True
        return obj.author == request.user
