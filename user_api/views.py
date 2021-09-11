import logging

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user_api.models import User
from user_api.serializers import UserSerializer

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
                #encoding token
                encoded_token = jwt.encode(
                    {"username" : serializers.data.get("username")},
                    "secret",
                    algorithm="HS256"
                    )
                # sending mail with encoded token
                subject = 'welcome to FundooNotes'
                message = f'Hi {serializers.data.get("username")}, thank you for registering in FundooNotes. click on the link below to get yourself verified\n http://127.0.0.1:8000/user/verify/{encoded_token}/'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [serializers.data.get("email"), ]
                send_mail( subject, message, email_from, recipient_list )
                logger.info(f"Registered user")

                return Response({"message":"Registered successfully","data":serializers.data["username"]},status=status.HTTP_201_CREATED)

            logger.error(f"serializer valiadation fails due to {serializers.errors}")
            return Response({"message":"User already exsists","data":serializers.errors},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error("internal server error while registering the user")
            print(e)
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

class Verification(APIView):

    """
    This api use to validate the user email is it correct or not
    """
    def get(self, request, token):
        
        try:
            decoded_token = jwt.decode(token,"secret",algorithms="HS256")
            user = User.objects.get(username=decoded_token.get("username"))
            user_data= UserSerializer(user)
            serializer = UserSerializer(user,data= user_data.data)
            if serializer.is_valid():
                serializer.set_verified(validated_data=serializer.data)
                return Response(
                    {
                        "message" : f'{serializer.data.get("username")} verfied',
                        "data": {"username":serializer.data.get("username")}
                    },
                    status=status.HTTP_202_ACCEPTED
                    )
            logger.error(f"failed to verify user due to {serializer.errors}")
            return Response(
                {
                    "message": "failed to verify user",
                    "data" : serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e :
            logger.error(f"Couldn`t register user due to {e}")
            return Response(
                {
                    "message": "failed to verify user",
                    "data" : serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
                )
