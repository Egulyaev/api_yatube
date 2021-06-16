from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter

from .views import PostViewSet, api_comments, api_comments_detail

router = SimpleRouter()
router.register('api/v1/posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/v1/api-token-auth/', views.obtain_auth_token),
    path('api/v1/posts/<int:pk>/comments/', api_comments),
    path('api/v1/posts/<int:pk>/comments/<int:pk2>/', api_comments_detail),
]
