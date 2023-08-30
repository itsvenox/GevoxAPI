# gevox_authentication views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response

from gevox_authentication.models import Follow, UserProfile
from .serializers import UserSerializer, profileSerializer
from rest_framework  import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from datetime import datetime

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser


@api_view(['POST'])
def loginAPI(request):
    email = request.data.get("email")
    password = request.data.get("password")
    username = request.data.get("username")

    if not email and not username:
        return Response({
            "code": 400,
            "response": "Please provide your email or username."
        })

    try:
        if email:
            user = User.objects.get(email=email)
        else:
            user = User.objects.get(username=username)
    except:
        return Response({
            "code": 404,
            "response": "User not found."
        })

    if not user.check_password(password):
        return Response({
            "code": 401,
            "response": "Invalid password."
        })

    # Generate or retrieve the authentication token
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({
        "code": 200,
        "response": "Login successful.",
        "details": {
            "time": datetime.now().strftime("%y/%m/%d - %H:%M:%S"),
            "token": token.key,
        }
    })


# Here is the signup API request
@api_view(['POST'])
def signupAPI(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        username = request.data.get('username')
        if User.objects.filter(username=username).exists():
            return Response({
                "code": 400,
                "response": "Username already exists."
                })
        
        # Save the user instance
        user = serializer.save()
        # Set the user's password
        user.set_password(request.data["password"])
        # Save the updated user instance
        user.save()
        profile_data = {
            "user": user,
            "profile_picture": None,  # Set to the user's profile picture if available
            "bio": ""  # Set to the user's bio if available
        }
        UserProfile.objects.create(**profile_data)
        # Create an authentication token
        token = Token.objects.create(user=user)
        return Response({
            "code": 201,
            "response": "User created successfully.",
            "details": {
                "time": datetime.now().strftime("%y/%m/%d - %H:%M:%S"),
                "user": serializer.data,
                "token": token.key
                }
            })
    else:
        return Response({
            "code": 400,
            "response": "A user with that username already exists."
            })


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
            "code": 200,
            "response": "Logout successful."
            })
    except Token.DoesNotExist:
        return Response({
            "code": 401,
            "response": "Invalid token."
            })



# Here is the Ban user API request
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
@api_view(['POST'])
def banUserAPI(request):
    username = request.data.get("username")
    try:
        user = User.objects.get(username=username)
        user.delete()  # Delete the user from the database
        return Response({
            "response": "User banned and deleted successfully.",
            "code" : 200
        })
    except User.DoesNotExist:
        return Response({
            "response": "User not found.",
            "code": 404
        })



@api_view(['GET'])
def userProfileAPI(request, pk):
    try:
        user_profile = UserProfile.objects.get(pk=pk)
        serializer = profileSerializer(user_profile)
        return Response(serializer.data)
    except UserProfile.DoesNotExist:
        return Response({
            "response": "User profile not found.",
            "code": 404
        })



# gevox_authentication views.py
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def followUserAPI(request, id):
    try:
        target_user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"response": "User not found.", "code": 404})
    
    if request.user == target_user:
        return Response({"response": "You can't follow yourself.", "code": 400})
    
    follow, created = Follow.objects.get_or_create(follower=request.user, following=target_user)
    
    if created:
        return Response({"response": "User followed successfully.", "code": 201})
    else:
        return Response({"response": "You are already following this user.", "code": 400})


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def unfollowUserAPI(request, id):
    try:
        target_user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"response": "User not found.", "code": 404})
    
    follow = Follow.objects.filter(follower=request.user, following=target_user)
    
    if follow.exists():
        follow.delete()
        return Response({"response": "User unfollowed successfully.", "code": 200})
    else:
        return Response({"response": "You are not following this user.", "code": 400})
