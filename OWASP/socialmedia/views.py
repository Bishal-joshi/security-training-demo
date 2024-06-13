from .models import Post, Comment
from django.shortcuts import get_object_or_404
import json
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


# secure coding guidelines
# code ma username password narakhne hardcoded / configuration
# logs ma pani halnu vayena sensetive data haru
# input validation chaiyo so that XSS nahos, data sanitize garne
# frontend ma validation ma var parnu hunnna, client side is never secure
# backend ma validation garnu parchha
# data store garda hash data store garnu paryo, password ni hash store garnu paryo


# Injection: orm ma matra var naparne, input validation garnu paryo

# broken authentication: permissions token ko validate garne,
# token chha vandaima sab access nadine,
# token ko authorize ko limit anusar matra dine token ni valdate garne

# secure coding design:
#

# CORS: jun sukai client bata req aauna nadine, euta client ko bata matra accept
# frontend and backend ko lagi configuration
#

# cookies banaune bela, secure only http only seetings haru hunchha, cookies secure banauna, etc flag banaune,
# cookie rotate, copy paste garyo ani req garyo

# .git halyo vane ani url ma sdasdas/something.html garyo vane tyo file ni aauchha
# file access dina ko lagi

# 123215.pdf

# url ma ../ garyo vane pachi ko file ni dekhinchha pachadi ko tyo rokna ko lagi
# error message ni development ma dekhaune tara production ma sakesamma detail stack trace nadine, path sabai hunchha
# server mai dump garne, console ma detail error nadekhaune

# database chhuttai thau chha vane database bahira bata access garna milcha
#

# class euta server to arko server ma pathauna class lai string ma convert garchha
#  and uta deserialize garne bela verify garnu paryo class modify ta vako chhaina or jpt code
# lekhera aako ta chhaina

# nginx host garda root bata vanda ni euta user lai privilage dine so that euta user bata matra hos
# root access payo vane sab le paula j garna ni, root user bata server run nagarne

# in python pickle garne, obj lai string ma convert and feri string lai obj ma

# class ViewUserPostsAPIView(APIView):
#     permission_classes = [CustomJWTAuthentication]

#     def get(self, request, user_id):
#         # Retrieve the user object using the provided user_id
#         try:
#             user = User.objects.get(id=user_id)
#         except Exception as e:
#             return Response({"message": "user doesnot exist"})

#         # Retrieve posts associated with the user
#         posts = Post.objects.filter(user=user)

#         # Extract required fields from each post and create a list of dictionaries
#         posts_data = []
#         for post in posts:
#             post_data = {
#                 'id': post.id,
#                 'user': post.user.email,  # Assuming you want to include user email
#                 'content': post.content,
#                 'is_public': post.is_public,
#                 'created_at': post.created_at
#             }
#             posts_data.append(post_data)

#         # Return the list of post data as a response
#         return Response({"posts": posts_data}, status=status.HTTP_200_OK)

class ViewUserPostsAPIView(APIView):
    permission_classes = [CustomJWTAuthentication]

    def get(self, request, user_id):
        # Retrieve the user object using the provided user_id
        try:
            user = User.objects.get(id=user_id)
        except Exception as e:
            return Response({"message": "user doesnot exist"})

        # Retrieve posts associated with the user
        posts = Post.objects.filter(user=user).order_by("-id")

        # Extract required fields from each post and create a list of dictionaries
        posts_data = []
        for post in posts:
            # Retrieve likes count for the post
            likes_count = post.likes.count()
            # Retrieve comments for the post
            comments = Comment.objects.filter(post=post)
            comments_data = []
            for comment in comments:
                comment_data = {
                    # 'user': comment.user.email,  # Assuming you want to include user email
                    'user': comment.user.name,  # Assuming you want to include user email
                    'content': comment.content,
                    'created_at': comment.created_at
                }
                comments_data.append(comment_data)

            post_data = {
                "id": post.id,
                'user': post.user.email,  # Assuming you want to include user email
                'content': post.content,
                'created_at': post.created_at,
                'likes_count': likes_count,
                'comments': comments_data,
                "name": post.user.name
            }
            posts_data.append(post_data)
        # Return the list of post data as a response
        return Response({"posts": posts_data}, status=status.HTTP_200_OK)


class ViewUserPostsWithEmailAPIView(APIView):
    permission_classes = [CustomJWTAuthentication]

    def get(self, request, user_email):
        # Retrieve the user object using the provided user_email
        try:
            user = User.objects.get(email=user_email)
        except Exception as e:
            return Response({"message": "user doesnot exist"})

        # Retrieve posts associated with the user
        posts = Post.objects.filter(user=user).order_by("-id")

        # Extract required fields from each post and create a list of dictionaries
        posts_data = []
        for post in posts:
            # Retrieve likes count for the post
            likes_count = post.likes.count()
            # Retrieve comments for the post
            comments = Comment.objects.filter(post=post)
            comments_data = []
            for comment in comments:
                comment_data = {
                    # 'user': comment.user.email,  # Assuming you want to include user email
                    'user': comment.user.name,  # Assuming you want to include user email
                    'content': comment.content,
                    'created_at': comment.created_at
                }
                comments_data.append(comment_data)

            post_data = {
                "id": post.id,
                'user': post.user.email,  # Assuming you want to include user email
                'content': post.content,
                'created_at': post.created_at,
                'likes_count': likes_count,
                'comments': comments_data,
                "name": post.user.name
            }
            posts_data.append(post_data)
        # Return the list of post data as a response
        return Response({"posts": posts_data}, status=status.HTTP_200_OK)


# class ViewAllPost(APIView):
#     permission_classes = [CustomJWTAuthentication]

#     def get(self, request):

#         # Retrieve posts associated with the user
#         posts = Post.objects.filter(is_public=True)
#         # Extract required fields from each post and create a list of dictionaries
#         posts_data = []
#         for post in posts:
#             post_data = {
#                 'name': post.user.name,  # Assuming you want to include user email
#                 'content': post.content,
#                 'created_at': post.created_at
#             }
#             posts_data.append(post_data)

#         # Return the list of post data as a response
#         return Response({"posts": posts_data}, status=status.HTTP_200_OK)


class ViewAllPost(APIView):
    permission_classes = [CustomJWTAuthentication]

    def get(self, request):

        # Retrieve posts associated with the user
        posts = Post.objects.filter(is_public=True).order_by("-id")
        # Extract required fields from each post and create a list of dictionaries
        posts_data = []
        for post in posts:
            # Retrieve likes count for the post
            likes_count = post.likes.count()
            # Retrieve comments for the post
            comments = Comment.objects.filter(post=post)
            comments_data = []
            for comment in comments:
                comment_data = {
                    'user': comment.user.name,  # Assuming you want to include user email
                    'content': comment.content,
                    'created_at': comment.created_at
                }
                comments_data.append(comment_data)

            post_data = {
                "id": post.id,
                'user': post.user.email,  # Assuming you want to include user email
                'content': post.content,
                'created_at': post.created_at,
                'likes_count': likes_count,
                'comments': comments_data,
                "name": post.user.name
            }
            posts_data.append(post_data)

        # Return the list of post data as a response
        return Response({"posts": posts_data}, status=status.HTTP_200_OK)


class A(APIView):
    def get(self, request):
        a = request.GET["apple"]
        return Response({"success": a})


# checklist deployed ko lagi
# frontend ko checklist, input validation
#  backend ko cors origin,


class LikePostAPIView(APIView):
    permission_classes = [CustomJWTAuthentication]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user:
            if request.user in post.likes.all():
                # If user already liked the post, unlike it
                post.likes.remove(request.user)
                liked = False
            else:
                # Like the post
                post.likes.add(request.user)
                liked = True
            return Response({'liked': liked, 'likes_count': post.likes.count()}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_403_FORBIDDEN)


class AddCommentAPIView(APIView):
    permission_classes = [CustomJWTAuthentication]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        content = request.data.get('content')
        if request.user:
            # Create a new comment
            Comment.objects.create(
                user=request.user, post=post, content=content)
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_403_FORBIDDEN)
