from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet  # api_comments, api_comments_detail
from .views import PostViewSet

router = DefaultRouter()
router.register('v1/posts', PostViewSet)
router.register(r'v1/posts/(?P<post_id>[0-9]+)/comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
