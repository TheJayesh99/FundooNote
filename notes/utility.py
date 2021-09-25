from user_api.models import User
import jwt
import redis
from django.conf import settings
from django.http import JsonResponse, QueryDict
from user_api.serializers import UserSerializer

from notes.models import Labels
from notes.serializers import LabelSerializer

redis_instence = redis.Redis(host=settings.REDIS_HOST,port=settings.REDIS_PORT)

class EncodeDecodeToken:
    
    """
    CLass to encode and decode the user token 
    """
    @staticmethod
    def decode_token(token):
        
        decoded_token = jwt.decode(
            token,
            settings.ENCODING_TYPE,
            algorithms="HS256"
        )
        return decoded_token


def verify_token(function):

    def wrapper(self,request):

        if 'HTTP_TOKEN' not in request.META:
            resp = JsonResponse({'message':'Token Not provided in header'})
            resp.status_code = 400
            return resp
        decode_token = EncodeDecodeToken.decode_token(request.META.get('HTTP_TOKEN'))
        redis_decode_token = EncodeDecodeToken.decode_token(redis_instence.get(decode_token.get("user_id")))
        if redis_decode_token.get("user_id") != decode_token.get("user_id"):
            resp = JsonResponse({
                'message':'login again',
                })
            resp.status_code = 401
            return resp
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data["user_id"] = decode_token.get("user_id")
        return function(self, request)
    return wrapper

def notes_converter(notes_list):
    
    """
    converts all the id into names
    """
    for notes in notes_list: 
        
        #converting all the labels id into its details
        label_list = []
        for label_id in notes.get("label"):
            label_details = LabelSerializer(Labels.objects.get(id = label_id))
            label_list.append(label_details.data)
        notes["label"] = label_list

        #converting all the labels id into its username
        collaborator_list = []
        for collaborator_id in notes.get("collaborators"):
            collaborator_details = UserSerializer(User.objects.get(id= collaborator_id))
            collaborator_list.append(collaborator_details.data.get("username"))
        notes["collaborators"] = collaborator_list
    return notes_list

def user_details(user_list):
    
    username_list = []
    for user_id in user_list:
        username_list.append(user_id.get("username"))
    return username_list
    