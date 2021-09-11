from rest_framework import  serializers
from user_api.models import User
import logging 

logging.basicConfig(filename="fundooNotes.log",filemode="a")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ["username","email","password","first_name","last_name","is_login","is_verified"] 

    def create_user(self,validation_data):
        
        try:

            new_user = User.objects.create_user(validation_data["username"],validation_data["email"],validation_data["password"])
            new_user.first_name = validation_data["first_name"]
            new_user.last_name = validation_data["last_name"]
            new_user.save()
        except Exception as e:
            logger.error("Error to create a user in seralizers")
            print(e)

    def set_verified(self, validated_data):

        user = User.objects.get(username = validated_data.get("username"))
        user.is_verified = True
        user.save()
        