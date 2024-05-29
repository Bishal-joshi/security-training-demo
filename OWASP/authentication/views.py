from django.conf import settings
from datetime import datetime, timedelta
import jwt
from django.db import connection
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import User
import hashlib
from django.contrib.auth import authenticate

# https://www.authgear.com/post/what-is-broken-access-control-vulnerability-and-how-to-prevent-it


class Register(APIView):
    def post(self, request):
        # Retrieve data from request
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        if (len(password) < 8):
            return JsonResponse({'error': 'Password should be of max length 8'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Hash the password before saving
        # hashed_password = make_password(password)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Create a new user instance
        user = User.objects.create(
            name=name, email=email, password=hashed_password)

        # Return a success response
        return JsonResponse({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)


# class Login(APIView):

#     def post(self, request):
#        # Retrieve data from request
#         email = request.data.get('email')
#         password = request.data.get('password')

#         # Find user by email
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return JsonResponse({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

#         # Verify password
        # hashed_password = hashlib.sha256(password.encode()).hexdigest()
#         if hashed_password != user.password:
#             return JsonResponse({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

#         # If password matches, return success response
#         return JsonResponse({'message': 'Login successful'}, status=status.HTTP_200_OK)

def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=1),  # Token expiration time
        'iat': datetime.utcnow()  # Token issued at time
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def verify_and_decode_jwt(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        # Handle token expiration
        return None
    except jwt.InvalidTokenError:
        # Handle invalid token
        return None


class Login(APIView):

    def post(self, request):
        # Retrieve data from request
        email = request.data.get('email')
        password = request.data.get('password')
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Construct SQL query using user inputs directly (vulnerable to SQL injection)
        sql_query = f"SELECT * FROM authentication_user WHERE email ='{email}' AND password ='{hashed_password}'"

        # Execute raw SQL query
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            row = cursor.fetchall()

            if (row.__len__() == 0):
                return JsonResponse({"error": "username password doesnot match"})
        try:
            user = User.objects.get(email=email)
            token = generate_jwt_token(user)
            # verify = verify_and_decode_jwt(token=token)
            # print(verify)
            row = row[0]
            user_object = {}
            user_object["id"] = row[0]
            user_object["name"] = row[1]
            user_object["email"] = row[2]

            # Return fetched row(s)
            return JsonResponse({'user': user_object, "token": token}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"row": row})

# login with this
# {
#     "name": "bishal",
#     "email": "bishaljoshi@gmail.com' OR 1=1;",
#     "password": "12345678"
# }
