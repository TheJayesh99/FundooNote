import jwt
import redis
from django.conf import settings
from django.http import JsonResponse

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
                "redis":str(redis_decode_token),
                "request":request.META.get('HTTP_TOKEN')
                })
            resp.status_code = 400
            return resp
        request.data["user_id"] = decode_token.get("user_id")
        return function(self, request)
    return wrapper

