from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework  import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User




# Here is the login api request
@api_view(['POST'])
def loginAPI(request):
    return Response({})



# Here is the signup api request
@api_view(['POST'])
def signupAPI(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data["username"])
        user.set_password(request.data["password"])
        user.save()
        token = Token.objects.create(user=user)
        return Response({
            "user": serializer.data,
            "token": token.key
        })
    else:
        return Response({"error":"User already exist."}, status=status.HTTP_400_BAD_REQUEST)


# Here is the delete user api request
@api_view(['POST'])
def deleteUserAPI(request):
    user = User.objects.get(username=request.data["username"])
    try:
        user.delete()
        return Response({
            "status":"User deleted successfuly.",
        })
    except:
        return Response({"error":"User not found."},
                        status=status.HTTP_401_UNAUTHORIZED)



# @api_view(['POST'])
# def loginAPI(request):
#     return Response({})