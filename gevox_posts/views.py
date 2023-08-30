# gevox_posts views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from gevox_posts.models import CommentModel, PostModel
from .serializers import PostSerializer, SparkSerializer
from rest_framework  import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createPostAPI(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        # Set the author field to the currently authenticated user
        serializer.validated_data['author'] = request.user
        # Create the post object
        post = serializer.save()
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
        post = PostModel.objects.get(post_id=post_id)
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
    posts = PostModel.objects.all().order_by('-createdAt')  # Order by descending date
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)



@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def likePostAPI(request, post_id):
    try:
        post = PostModel.objects.get(post_id=post_id)
        user = request.user
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            return Response({"response": "Post unliked.", "code": 200})
        else:
            post.likes.add(user)
            return Response({"response": "Post liked.", "code": 200})
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
@api_view(['POST'])
def addCommentAPI(request, post_id):
    try:
        post = PostModel.objects.get(post_id=post_id)
        content = request.data.get('content')
        if content:
            comment = CommentModel.objects.create(post=post, user=request.user, content=content)
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



# edit comment api

