from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework  import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from datetime import datetime


# Here is the login API request
@api_view(['POST'])
def loginAPI(request):
    email = request.data.get("email")
    password = request.data.get("password")
    
    # Check if password is provided
    if not password:
        return Response({
            "response": "Please provide your password."
            }, status=status.HTTP_400_BAD_REQUEST
        )
    
    if not email:
        try: 
            username = request.data.get("username")
        except KeyError:
            return Response({
                "response": "Please provide your email or username."
                }, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Retrieve the user based on the provided email or username
        user = User.objects.get(email=email) if email else User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({
            "response": "User not found."
        }, status=status.HTTP_404_NOT_FOUND)

    if not user.check_password(password):
        return Response({
            "response": "Invalid password."
        }, status=status.HTTP_401_UNAUTHORIZED)

    # Generate or retrieve the authentication token
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({
        "response": "Login successful.",
        "details": {
            "time": datetime.now().strftime("%y/%m/%d - %H:%M:%S"),
            "token": token.key
        }
    }, status=status.HTTP_200_OK)


# Here is the signup API request
@api_view(['POST'])
def signupAPI(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Save the user instance
        user = serializer.save()
        # Set the user's password
        user.set_password(request.data["password"])
        # Save the updated user instance
        user.save()
        # Create an authentication token
        token = Token.objects.create(user=user)
        return Response({
            "response": "User created successfully.",
            "details": {
                "time": datetime.now().strftime("%y/%m/%d - %H:%M:%S"),
                "user": serializer.data,
                "token": token.key
            }
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({
            "response": "User already exists."
        }, status=status.HTTP_400_BAD_REQUEST)


# Here is the delete user API request
@api_view(['POST'])
def deleteUserAPI(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        
        # Check if email, username, and password are provided
        if not (email and password and username):
            return Response({
                "response": "Email, username, and password are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the user based on the provided email
        user = User.objects.get(email=email)

        if not user.check_password(password):
            return Response({
                "response": "Invalid password."
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        if user.get_username() != username:
            return Response({
                "response": "Invalid username."
                }, status=status.HTTP_401_UNAUTHORIZED)

        # Delete the user
        user.delete()
        return Response({
            "time": datetime.now().strftime("%y/%m/%d - %H:%M:%S"),
            "response": "User deleted successfully."
        }, status=status.HTTP_202_ACCEPTED)
    except User.DoesNotExist:
        return Response({
            "response": "User not found."
        }, status=status.HTTP_404_NOT_FOUND)




# @api_view(['POST'])
# def loginAPI(request):
#     return Response({})