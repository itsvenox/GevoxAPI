# gevox_authentication views.py
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from gevox_authentication.models import Follow, UserProfile
from gevox_posts.models import PostModel
from gevox_posts.serializers import PostSerializer
from .serializers import UserSerializer, UserProfileSerializer
from rest_framework  import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from datetime import datetime

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import AnonymousUser

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
        
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({
                "code": 400,
                "response": "Email already exists."
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





@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def currentUserAPI(request):
    # Check if the user is authenticated
    if not isinstance(request.user, AnonymousUser):
        user_profile = UserProfile.objects.get(user=request.user)
        # posts = PostModel.objects.filter(author=request.user)

        user_data = {
            'id': user_profile.user.id,
            'username': user_profile.user.username,
            'email': user_profile.user.email,
            'profile_picture': user_profile.profile_picture if user_profile.profile_picture else None,
            'joined_date': user_profile.user.date_joined,
            'bio': user_profile.bio,
            # 'posts': PostSerializer(posts, many=True).data  # Serialize the user's posts
        }

        return Response({
            "code": 200,
            "details": user_data
        })
    else:
        return Response({
            "response": "User not authenticated.",
            "code": 401
        })


@api_view(['GET'])
def userProfileAPI(request, pk):
    if not isinstance(request.user, AnonymousUser):
        user_profile = UserProfile.objects.get(id=pk)
        posts = PostModel.objects.filter(author=pk)

        user_data = {
            'id': user_profile.user.id,
            'username': user_profile.user.username,
            # 'email': user_profile.user.email,
            'profile_picture': user_profile.profile_picture if user_profile.profile_picture else None,
            'joined_date': user_profile.user.date_joined,
            'bio': user_profile.bio,
            'posts': PostSerializer(posts, many=True).data  # Serialize the user's posts
        }

        return Response({
            "code": 200,
            "details": user_data
        })
    else:
        return Response({
            "response": "User not authenticated.",
            "code": 401
        })




# Here is the Logout user API request
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def logoutAPI(request):
    token = request.headers.get('Authorization')
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







# gevox_authentication views.py
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def followUserAPI(request, id):
    try:
        target_user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"response": "User not found.", "code": 404})
    
    if request.user == target_user:
        return Response({"response": "You can't follow yourself.", "code": 400})
    
    follow, created = Follow.objects.get_or_create(follower=request.user, following=target_user)
    
    if created:
        request.user.userprofile.reputation += 1
        request.user.userprofile.save()
        upgrade_user_level(request.user.userprofile)
        return Response({"response": "User followed successfully.", "code": 201})
    else:
        return Response({"response": "You are already following this user.", "code": 400})


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def unfollowUserAPI(request, id):
    try:
        target_user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"response": "User not found.", "code": 404})
    
    follow = Follow.objects.filter(follower=request.user, following=target_user)
    
    if follow.exists():
        follow.delete()
        request.user.userprofile.reputation -= 1
        request.user.userprofile.save()
        return Response({"response": "User unfollowed successfully.", "code": 200})
    else:
        return Response({"response": "You are not following this user.", "code": 400})




def upgrade_user_level(user_profile):
    reputation = user_profile.reputation

    if reputation < 5:
        user_profile.level = 1
    elif reputation < 25:
        user_profile.level = 2
    elif reputation < 50:
        user_profile.level = 3
    elif reputation < 100:
        user_profile.level = 4
    elif reputation < 200:
        user_profile.level = 5
    elif reputation < 400:
        user_profile.level = 6
    elif reputation < 550:
        user_profile.level = 7
    elif reputation < 700:
        user_profile.level = 8
    elif reputation < 950:
        user_profile.level = 9
    elif reputation < 1200:
        user_profile.level = 10

    user_profile.save()