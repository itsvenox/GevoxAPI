# gevox_posts views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from gevox_authentication.views import upgrade_user_level
from gevox_posts.models import CommentModel, PostModel
from .serializers import CommentSerializer, PostSerializer, SparkSerializer
from rest_framework  import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from gevox_authentication.models import UserProfile




@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def createPostAPI(request):
    serializer = PostSerializer(data=request.data)

    if serializer.is_valid():
        author_id = request.data.get("author")
        try:
            author = User.objects.get(pk=author_id)
        except User.DoesNotExist:
            return Response({
                "response": "Invalid author ID.",
                "code": 400
            })
        serializer.validated_data['author'] = author

        # Create the post object
        post = serializer.save()

        # Update user level
        request.user.userprofile.reputation += 5
        request.user.userprofile.save()
        upgrade_user_level(request.user.userprofile)

        return Response({
            "response": "Post created successfully.",
            "post": serializer.data,
            "code": 201
        })
    else:
        return Response({
            "response": "Invalid data.",
            "errors": serializer.errors,
            "code": 400
        })






@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def deletePostAPI(request, post_id):
    try:
        post = PostModel.objects.get(id=post_id, author=request.user.id)
        post.delete()
        return Response({"response": "Post deleted successfully.", "code": 301})
    except PostModel.DoesNotExist:
        return Response({"response": "Post not found.", "code": 404})
    except Exception as e:
        return Response({"response": str(e), "code": 500})


@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def getPostAPI(request, post_id):
    try:
        post = PostModel.objects.get(id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    except PostModel.DoesNotExist:
        return Response({"response": "Post not found.", "code": 404})
    except Exception as e:
        return Response({"response": str(e), "code": 400})




@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def getAllPostsAPI(request):
    try:
        posts = PostModel.objects.all().order_by('-created_at')  # Order by descending date
        serializer = PostSerializer(posts, many=True)

        # Upgrade user level based on reputation if the user is authenticated
        if request.user.is_authenticated:
            upgrade_user_level(request.user.userprofile)

        return Response({"code": 200, "response": "Posts Found.", "posts": serializer.data})
    except Exception as e:
        return Response({"response": str(e), "code": 500})
    



@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def likePostAPI(request, post_id):
    try:
        if request.user.is_authenticated:
            post = PostModel.objects.get(id=post_id)
            user = request.user
            if post.likes.filter(id=user.id).exists():
                post.likes.remove(user)
                post.author.userprofile.reputation -= 1
                post.author.userprofile.save()
                request.user.userprofile.reputation -= 1
                request.user.userprofile.save()
                return Response({"response": "Post unliked.", "code": 200})
            else:
                post.likes.add(user)
                post.author.userprofile.reputation += 1
                post.author.userprofile.save()
                request.user.userprofile.reputation += 1
                request.user.userprofile.save()
                upgrade_user_level(request.user.userprofile)
                return Response({"response": "Post liked.", "code": 200})
        else:
            return Response({"response": "You must be logged in to perform this action.", "code": 302})
    except PostModel.DoesNotExist:
        return Response({"response": "Post not found.", "code": 404})
    except Exception as e:
        return Response({"response": str(e), "code": 400})




@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
@api_view(['POST'])
def newSparkAPI(request):
    serializer = SparkSerializer(data=request.data)
    if serializer.is_valid():
        newSpark = request.data.get("spark")
        serializer.save()
        return Response({"response": "add successfuly", "code": 200})


# add comment api 
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def addCommentAPI(request, post_id):
    try:
        post = PostModel.objects.get(id=post_id)
        content = request.data.get('content')
        if content:
            comment = CommentModel.objects.create(post=post, user=request.user, content=content)
            post.author.userprofile.reputation += 2
            post.author.userprofile.save()
            request.user.userprofile.reputation += 2
            request.user.userprofile.save()
            upgrade_user_level(request.user.userprofile)
            return Response({"response": "Comment added successfully.", "code": 201})
        else:
            return Response({"response": "Comment text is required.", "code": 400})
    except PostModel.DoesNotExist:
        return Response({"response": "Post not found.", "code": 404})
    except Exception as e:
        return Response({"response": str(e), "code": 400})


# delete comment api
@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def deleteCommentAPI(request, comment_id):
    try:
        comment = CommentModel.objects.get(id=comment_id, user=request.user)
        comment.delete()
        return Response({"response": "Comment deleted successfully.", "code": 200})
    except CommentModel.DoesNotExist:
        return Response({"response": "Comment not found.", "code": 404})
    except Exception as e:
        return Response({"response": str(e), "code": 400})



@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def getCommentsAPI(request, post_id):
    try:
        comments = CommentModel.objects.filter(post=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response({"response": "Comments found.", "code": 200, "comments": serializer.data})
    except CommentModel.DoesNotExist:
        return Response({"response": "Comments not found.", "code": 200})
    except Exception as e:
        return Response({"response": str(e), "code": 400})


