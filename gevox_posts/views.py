from rest_framework.decorators import api_view
from rest_framework.response import Response

from gevox_posts.models import PostModel
from .serializers import PostSerializer
from rest_framework  import status
from rest_framework.authtoken.models import Token


from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated



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
                "response": "Invalid author ID."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Assign the author instance to the serializer's data
        serializer.validated_data['author'] = author

        # Create the post object
        post = serializer.save()
        return Response({
            "response": "Post created successfully.",
            "post": serializer.data
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({
            "response": "Invalid data.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def deletePostAPI(request, pk):
    try:
        post = PostModel.objects.get(id=pk, author=request.user.id)
        post.delete()
        return Response({"response": "Post deleted successfully."}, status=status.HTTP_302_FOUND)
    except PostModel.DoesNotExist:
        return Response({"response": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"response": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def getPostAPI(request, pk):
    try:
        post = PostModel.objects.get(id=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except PostModel.DoesNotExist:
        return Response({"response": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"response": str(e)}, status=status.HTTP_400_BAD_REQUEST)




@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def getAllPostsAPI(request):
    try:
        posts = PostModel.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"response": str(e)}, status=status.HTTP_400_BAD_REQUEST)
