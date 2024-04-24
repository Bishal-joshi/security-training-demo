from authentication.models import User
from .models import Post
from rest_framework import status
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import CustomJWTAuthentication


class MyProtectedView(APIView):
    permission_classes = [CustomJWTAuthentication]

    def get(self, request, format=None):
        # This view will only be accessible if the token is valid
        return Response({"message": "This is a protected view"})

# {
#     "content":"hi man k chha",
#     "is_public":true
# }
# http://127.0.0.1:8000/socialmedia/post/

#

# yo halnu pachi at last for xss attack
# {
#     "content":"<script>alert('hi')</script>",
#     "is_public":true
# }


class CreatePostAPIView(APIView):
    permission_classes = [CustomJWTAuthentication]

    def post(self, request):
        user = request.user  # Assuming user is authenticated
        content = request.data.get('content')
        is_public = request.data.get('is_public', True)

        if content:
            post = Post.objects.create(
                user=user, content=content, is_public=is_public)
            return Response({"message": "Post created successfully", "post_id": post.id}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Content is required"}, status=status.HTTP_400_BAD_REQUEST)

# http://127.0.0.1:8000/socialmedia/posts/2


class ViewUserPostsAPIView(APIView):
    permission_classes = [CustomJWTAuthentication]

    def get(self, request, user_id):
        # Retrieve the user object using the provided user_id
        try:
            user = User.objects.get(id=user_id)
        except Exception as e:
            return Response({"message": "user doesnot exist"})

        # Retrieve posts associated with the user
        posts = Post.objects.filter(user=user)

        # Extract required fields from each post and create a list of dictionaries
        posts_data = []
        for post in posts:
            post_data = {
                'id': post.id,
                'user': post.user.email,  # Assuming you want to include user email
                'content': post.content,
                'is_public': post.is_public,
                'created_at': post.created_at
            }
            posts_data.append(post_data)

        # Return the list of post data as a response
        return Response({"posts": posts_data}, status=status.HTTP_200_OK)
