# views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response

from gevox_posts.models import PostModel
from .serializers import PostSerializer, SparkSerializer
from rest_framework  import status
from rest_framework.authtoken.models import Token


from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser



from django.contrib.auth.models import User

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

        # Assign the author instance to the serializer's data
        serializer.validated_data['author'] = author

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
def deletePostAPI(request, pk):
    try:
        post = PostModel.objects.get(id=pk, author=request.user.id)
        post.delete()
        return Response({"response": "Post deleted successfully.", "code": 301})
    except PostModel.DoesNotExist:
        return Response({"response": "Post not found.", "code": 404})
    except Exception as e:
        return Response({"response": str(e), "code": 500})


@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def getPostAPI(request, pk):
    try:
        post = PostModel.objects.get(id=pk)
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
        posts = PostModel.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"response": str(e), "code": 301})



@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def likePostAPI(request, pk):
    try:
        post = PostModel.objects.get(id=pk)
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