
from django.urls import path
from .views import MyProtectedView, CreatePostAPIView, ViewUserPostsAPIView

urlpatterns = [
    path('test/', MyProtectedView.as_view(), name='test'),
    path('post/', CreatePostAPIView.as_view(), name='post'),
    path('posts/<int:user_id>/', ViewUserPostsAPIView.as_view(),
         name='view_user_posts'),
]
