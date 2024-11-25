# these are the rest_framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated ,AllowAny
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError


from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

from .models import Users
from .serializers import UserSerializer

# Create your views here.
class UserView(APIView):
    def get(self, request, name=None):
        if name is not None:
            try:
                user = Users.objects.get(username=name)
                serializer = UserSerializer(user)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Users.DoesNotExist:
                raise Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
        else:
            users = Users.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, name):
        try:
            user = Users.objects.get(username=name)
        except Users.DoesNotExist:
            raise NotFound("User not found")

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, name):
        try:
            user = Users.objects.get(username=name)
        except Users.DoesNotExist:
            raise NotFound("User not found")

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, name):
        try:
            user = Users.objects.get(username=name)
        except Users.DoesNotExist:
            raise NotFound("User not found")

        user.delete()
        return Response({"Message":"User deleted successfully"},status=status.HTTP_204_NO_CONTENT)
    







    # def post(self, request):
#         # username = request.data.get('username')
#         # password = request.data.get('password')

#         # try:
#         #     user = Users.objects.get(username=username)
#         # except Users.DoesNotExist:
#         #     return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#         # if user.password == password:
#         #     token, created = Token.objects.get_or_create(user=user)
#         #     return Response({"token": token.key}, status=status.HTTP_200_OK)
#         # else:
#         #     return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#         # username = request.data['username']
#         # password = request.data['password']

#         # if not username or not password:
#         #     return Response({"message": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

#         # # Print for debugging
#         # print(f"Attempting login for user: {username} with password: {password}")


#         # user=authenticate(request,username=username, password=password)
#         # if user is not None:
#         #     token, created = Token.objects.get_or_create(user=user)
#         #     return Response({"token": token.key}, status=status.HTTP_200_OK)
#         # return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # username = request.data.get('username')
        # password = request.data.get('password')

        # print(f"Attempting login for user: {username} with password: {password}")

        # if not username or not password:
        #     return Response({"message": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # # Authenticate using the custom backend
        # user=Users.objects.get(username=username)

        # print(check_password(password, user.password))
        # user = authenticate(request, username=username, password=password)
        
        # if user is not None:
        #     token, created = Token.objects.get_or_create(user=user)
        #     return Response({"token": token.key}, status=status.HTTP_200_OK)

        # return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# from django.contrib.auth.models import Users

# class LoginView(APIView):
#     def post(self, request):
#         # Get username and password from the request data
#         username = request.data.get('username')
#         password = request.data.get('password')

#         if not username or not password:
#             return Response({"message": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # Retrieve the user from the database
#             user = Users.objects.get(username=username)
#         except Users.DoesNotExist:
#             return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#         # Check if the password matches the hashed password stored in the database
#         if not check_password(password, user.password):
#             return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#         # Attempt to retrieve the token or create a new one if it doesn't exist
#         try:
#             token, created = Token.objects.get_or_create(user=user)
#             if created:
#                 print(f"New token created for user: {user.username}")
#             else:
#                 print(f"Token already exists for user: {user.username}")
#             return Response({"token": token.key}, status=status.HTTP_200_OK)
#         except IntegrityError as e:
#             # Handle any database integrity issues (e.g. foreign key errors)
#             print(f"IntegrityError occurred: {e}")
#             return Response({"message": "Token creation failed due to database integrity error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        print(user)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)