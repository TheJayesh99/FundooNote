import pytest
from rest_framework.reverse import reverse
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