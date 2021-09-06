from django.contrib.auth.models import User
from user_api.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate

# Create your views here.

class Register(APIView):

    """
    Class to register user in user model
    """
    def get(self, request):

        return Response(f"Welcome to registration plz register")

    def post(self, request):

        serializers = UserSerializer(data = request.data)
        if serializers.is_valid():
            new_user = User.objects.create_user(serializers.data["username"],serializers.data["email"],serializers.data["password"])
            new_user.first_name = serializers.data["first_name"]
            new_user.last_name = serializers.data["last_name"]
            new_user.save()
            print(serializers.data["first_name"],serializers.data["last_name"])
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):

    """
    Class to validate login of user
    """
    def get(self, request):

        return Response(f"Welcome to login page")

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username,password=password)
        if user != None:
            return Response("logged in successfully",status= status.HTTP_202_ACCEPTED)
        return Response("invalid details",status=status.HTTP_400_BAD_REQUEST)