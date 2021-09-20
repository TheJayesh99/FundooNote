import pytest
from mixer.backend.django import mixer
from rest_framework.reverse import reverse
from user_api.models import User
from user_api.utility import EncodeDecodeToken
from user_api.serializers import UserSerializer

pytestmark = pytest.mark.django_db

class TestUser:

    def test_registration_of_user(self, client):

        url = reverse("user:register")
        user = {
            "username": "jayesh34",
            "password": "jay_password",
            "email": "jayeshm.csmit@gmail.com",
            "first_name": "jay",
            "last_name": "mali"
            }
        response = client.post(url, user)
        assert response.status_code == 201
    
    def test_resgistration_of_user_with_same_username(self, client):

        url = reverse("user:register")
        user = mixer.blend(User, username='jayesh34') 
        user.save()
        new_user = {
            "username": "jayesh34",
            "password": "jay_password",
            "email": "jayeshm.csmit@gmail.com",
            "first_name": "jay",
            "last_name": "mali"
            }
        response = client.post(url,new_user)
        assert response.status_code == 400

    def test_user_is_verified_should_login(self, client):

        user = User.objects.create_user("jayesh34","jay@mail.com","jay_password")
        user.is_verified = True
        user.save()
        data = {
            "username":"jayesh34",
            "password":"jay_password",
        }
        url = reverse("user:login")
        response = client.post(url,data)
        assert response.status_code == 202
    
    def test_if_user_is_not_verified(self, client):

        User.objects.create_user("jayesh","jay@mail.com","jay_password")
        data = {
            "username":"jayesh",
            "password":"jay_password"
        }
        url = reverse("user:login")
        response = client.post(url,data)
        assert response.status_code == 400

    def test_user_is_verified_but_invalid_details(self, client):

        user = User.objects.create_user("jayesh34","jay@mail.com","jay_password")
        user.is_verified = True
        user.save()
        data = {
            "username":"jayesh34",
            "password":"jay_password2",
        }
        url = reverse("user:login")
        response = client.post(url,data)
        assert response.status_code == 500

    def test_user_must_verify_himself_before_login(self, client):

        user = mixer.blend(User, username="jayesh",password="jay_password")
        encoded_token = EncodeDecodeToken.encode_token(serializers=UserSerializer(user))
        url = f'http://127.0.0.1:8000/user/verify/{encoded_token}/'
        response = client.get(url)
        assert response.status_code == 202
