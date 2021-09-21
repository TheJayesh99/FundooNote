import logging

import redis
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import BadHeaderError, send_mail
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from user_api.models import User
from user_api.serializers import UserSerializer
from user_api.utility import EncodeDecodeToken ,redis_instence

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
            if serializers.is_valid(raise_exception=True):
                serializers.create_user(validation_data= serializers.data)
                #encoding token
                encoded_token = EncodeDecodeToken.encode_token(serializers)
                # sending mail with encoded token
                subject = 'welcome to FundooNotes'
                message = f'Hi {serializers.data.get("username")}, thank you for registering in FundooNotes. click on the link below to get yourself verified\n http://127.0.0.1:8000/user/verify/{encoded_token}/'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [serializers.data.get("email"), ]
                send_mail( subject, message, email_from, recipient_list )
                logger.info(f"Registered user")

                return Response({"message":"Registered successfully","data":serializers.data["username"]},status=status.HTTP_201_CREATED)
        
        except ValidationError:
            logger.error("validation failed while registering the user")
            return Response(
                {
                    "message":"Validation failed",
                    "data":serializers.errors
                },
                status=status.HTTP_400_BAD_REQUEST
                )

        except BadHeaderError:
            logger.error("Invalid header found while sending mail")
            return Response(
                {
                    "message":"Invalid header found"
                },
                status=status.HTTP_406_NOT_ACCEPTABLE
                )
        
        except Exception as e:
            logger.error("internal server error while registering the user")
            return Response(
                {
                    "message":"internal server error"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

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
            if user != None and user.is_verified :
                serializers = UserSerializer(user)
                encoded_token = EncodeDecodeToken.encode_token(serializers)
                logger.info(f"logged in successfully by {serializers.data.get('id')}")
                redis_instence.set(serializers.data.get('id'),encoded_token)
                return Response({"message":"logged in successfully","data":{"token":encoded_token}},status= status.HTTP_202_ACCEPTED)

            elif not user.is_verified :
                return Response({"message":"user is not verified","data":user.id},status= status.HTTP_400_BAD_REQUEST)
            logger.warning("invalid login details")
            return Response(
                {
                    "message":"invalid details"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
    
        except Exception as e:
            logger.error(f"internal server error while login by the user {e}")
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Verification(APIView):

    """
    This api use to validate the user email is it correct or not
    """
    def get(self, request, token):
        
        try:
            decoded_token = EncodeDecodeToken.decode_token(token)
            user = User.objects.get(username=decoded_token.get("username"))
            user_data= UserSerializer(user)
            serializer = UserSerializer(user,data= user_data.data)
            if serializer.is_valid(raise_exception=True):
                serializer.set_verified(validated_data=serializer.data)
                return Response(
                    {
                        "message" : f'{serializer.data.get("username")} verfied',
                        "data": {"username":serializer.data.get("username")}
                    },
                    status=status.HTTP_202_ACCEPTED
                    )

        except ValidationError:
            logger.error("validation failed while verify the user")
            return Response(
                {
                    "message":"Validation failed",
                    "data":serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e :
            logger.error(f"Couldn`t verify user due to {e}")
            return Response(
                {
                    "message": "failed to verify user",
                },
                status=status.HTTP_400_BAD_REQUEST
                )
                