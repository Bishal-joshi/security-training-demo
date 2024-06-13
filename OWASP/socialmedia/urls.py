
from django.urls import path
from .views import MyProtectedView, CreatePostAPIView, ViewUserPostsAPIView, ViewUserPostsWithEmailAPIView, ViewAllPost, AddCommentAPIView, LikePostAPIView, A

urlpatterns = [
    path('test/', MyProtectedView.as_view(), name='test'),
    path('post', CreatePostAPIView.as_view(), name='post'),
    path('posts/<int:user_id>/', ViewUserPostsAPIView.as_view(),
         name='view_user_posts'),

    path('posts/<str:user_email>/', ViewUserPostsWithEmailAPIView.as_view(),
         name='view_user_posts'),
    path("posts", ViewAllPost.as_view()),


    path("a", A.as_view()),

    path("like/<int:post_id>", LikePostAPIView.as_view()),
    path("comment/<int:post_id>", AddCommentAPIView.as_view())

]
