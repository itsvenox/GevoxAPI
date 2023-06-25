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
            "response":"User created successfuly.",
            "details":{
                "user": serializer.data,
                "token": token.key
                }
            },
            status=status.HTTP_201_CREATED
        )
    else:
        return Response({
            "response":"User already exist."
            },
            status=status.HTTP_400_BAD_REQUEST
        )


# Here is the delete user api request
@api_view(['POST'])
def deleteUserAPI(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        
        if not email or not password or not username:
            return Response({
                "response": "email, username and password are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=email)

        ##########################################
        if not user.check_password(password):
            return Response({
                "response": "Invalid Password."
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.get_username() == username:
            return Response({
                "response": "Invalid Username."
            }, status=status.HTTP_401_UNAUTHORIZED)
        ###########################################

        try:
            user.delete()
            return Response({
                "response": "User deleted successfully."
            }, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({
                "response": str(e)
            }, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({
            "response": "User not found."
        }, status=status.HTTP_404_NOT_FOUND)




# @api_view(['POST'])
# def loginAPI(request):
#     return Response({})