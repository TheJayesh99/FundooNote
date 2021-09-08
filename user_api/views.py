from user_api.models import User
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

        try:
            serializers = UserSerializer(data = request.data)
            if serializers.is_valid():
                serializers.create_user(validation_data= request.data)
                return Response(serializers.data,status=status.HTTP_201_CREATED)
            return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(serializers.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Login(APIView):

    """
    Class to validate login of user
    """
    def get(self, request):

        return Response(f"Welcome to login page")

    def post(self, request):

        try:
            username = request.data.get("username")
            password = request.data.get("password")
            user = authenticate(username=username,password=password)
            if user != None:
                return Response("logged in successfully",status= status.HTTP_202_ACCEPTED)
            return Response("invalid details",status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response("Invalid details",status=status.HTTP_500_INTERNAL_SERVER_ERROR)