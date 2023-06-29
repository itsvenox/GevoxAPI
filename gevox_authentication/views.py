from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework  import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from datetime import datetime

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser


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
        username = request.data.get('username')
        if User.objects.filter(username=username).exists():
            return Response({
                "response": "Username already exists."
            }, status=status.HTTP_400_BAD_REQUEST)
        
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
            "response": "A user with that username already exists."
        }, status=status.HTTP_400_BAD_REQUEST)



# Here is the Logout user API request
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def logoutAPI(request):
    token = request.headers.get('Authorization').split(' ')[1]
    try:
        # Find the token in the database
        token_obj = Token.objects.get(key=token)
        token_obj.delete()
        return Response({
            "response": "Logout successful."
        }, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({
            "response": "Invalid token."
        }, status=status.HTTP_401_UNAUTHORIZED)





# Here is the Ban user API request
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
@api_view(['POST'])
def banUserAPI(request):
    username = request.data.get("username")
    try:
        user = User.objects.get(username=username)
        user.is_active = False  # Ban the user by deactivating their account
        user.delete()  # Delete the user from the database
        return Response({
            "response": "User banned and deleted successfully."
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({
            "response": "User not found."
        }, status=status.HTTP_404_NOT_FOUND)
