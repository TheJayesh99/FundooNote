from user_api.models import User
from user_api.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
import logging 

logging.basicConfig(filename="fundooNotes.log",filemode="a")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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
                serializers.create_user(validation_data= serializers.data)
                logger.info(f"Registered user")
                return Response({"message":"Registered successfully","data":serializers.data["username"]},status=status.HTTP_201_CREATED)

            logger.error(f"serializer valiadation fails due to {serializers.errors}")
            return Response({"message":"User already exsists","data":serializers.errors},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error("internal server error while registering the user")
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                logger.info(f"logged in successfully by {user.id}")
                return Response({"message":"logged in successfully","data":user.id},status= status.HTTP_202_ACCEPTED)
            
            logger.warning("invalid login details")
            return Response("invalid details",status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error("internal server error while login by the user")
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)