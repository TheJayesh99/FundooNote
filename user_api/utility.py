import jwt
import redis
from django.conf import settings


class EncodeDecodeToken:
    
    """
    Method to check user is logined and verified himself
    """
    @staticmethod
    def encode_token(serializers):

        encoded_token = jwt.encode(
                    { "user_id":serializers.data.get("id"), "username":serializers.data.get("username") },
                    settings.ENCODING_TYPE,
                    algorithm="HS256"
                )
        return encoded_token

    @staticmethod
    def decode_token(token):

        decoded_token = jwt.decode(
            token,
            settings.ENCODING_TYPE,
            algorithms="HS256"
        )
        return decoded_token

redis_instence = redis.Redis(host=settings.REDIS_HOST,port=settings.REDIS_PORT)
