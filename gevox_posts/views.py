from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from gevox_posts.models import PostModel
from .serializers import PostSerializer
from rest_framework  import status
from rest_framework.authtoken.models import Token

from datetime import datetime

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated



from django.contrib.auth.models import User

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


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated])
def deletePostAPI(request, pk):
    try:
        post = PostModel.objects.get(id=pk, author=request.user.id)
        post.delete()
        return Response({"response": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except PostModel.DoesNotExist:
        return Response({"response": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"response": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
