import json

import pytest
from rest_framework.reverse import reverse
from user_api.models import User

pytestmark = pytest.mark.django_db

class TestNotes:

    def test_to_add_notes_of_particular_user(self, client):
        
        #creating a user
        user = User.objects.create_user("jayesh34","jay@mail.com","jay_password")
        user.is_verified = True
        user.save()
        #logging the user
        login_data = {
            "username":"jayesh34",
            "password":"jay_password",
        }
        url = reverse("user:login")
        response = client.post(url,login_data)
        json_data = json.loads(response.content)
        token = json_data.get('data').get("token")
        #adding notes
        notes_data = {
            "title":"This is my first note",
            "description":"this is my first note"
        }
        url= reverse("note:notes")
        header = {
            "HTTP_TOKEN":token,
        }
        response = client.post(url, notes_data, content_type='application/json' , **header)
        assert response.status_code == 201

    def test_to_fetch_notes_added_by_particular_user(self, client):

        #creating user
        user = User.objects.create_user("jayesh34","jay@mail.com","jay_password")
        user.is_verified = True
        user.save()
        #logging the user
        login_data = {
            "username":"jayesh34",
            "password":"jay_password",
        }
        url = reverse("user:login")
        response = client.post(url,login_data)
        json_data = json.loads(response.content)
        token = json_data.get('data').get("token")
        #adding notes
        notes_data = {
            "title":"This is my first note",
            "description":"this is my first note",
            "labels":["comic","sci-fi"]
        }
        url= reverse("note:notes")
        header = {
            "HTTP_TOKEN":token,
        }
        client.post(url, notes_data , **header)
        #fetching the note added by user
        response = client.get(url, **header)
        assert response.status_code == 200

    def test_to_update_exsisting_note(self, client):

        #creating user
        user = User.objects.create_user("jayesh34","jay@mail.com","jay_password")
        user.is_verified = True
        user.save()
        #logging the user
        login_data = {
            "username":"jayesh34",
            "password":"jay_password",
        }
        url = reverse("user:login")
        response = client.post(url,login_data)
        json_data = json.loads(response.content)
        token = json_data.get('data').get("token")
        #adding notes
        notes_data = {
            "title":"This is my first note",
            "description":"this is my first note",
        }
        url= reverse("note:notes")
        header = {
            "HTTP_TOKEN":token,
        }
        response = client.post(url, notes_data, content_type='application/json' , **header)
        json_data = json.loads(response.content)
        id = json_data.get('data').get("note")[0].get("id")
        #updating exsisting note
        updated_note_data = {
            "title":"This is my first note",
            "description":"this is my updated note",
            "id":int(id)
        }
        response = client.put(url, updated_note_data, content_type='application/json', **header)
        assert response.status_code == 202

    def test_to_delete_an_exsisting_note(self, client):

        #creating user
        user = User.objects.create_user("jayesh34","jay@mail.com","jay_password")
        user.is_verified = True
        user.save()
        #logging the user
        login_data = {
            "username":"jayesh34",
            "password":"jay_password",
        }
        url = reverse("user:login")
        response = client.post(url,login_data)
        json_data = json.loads(response.content)
        token = json_data.get('data').get("token")
        #adding notes
        notes_data = {
            "title":"This is my first note",
            "description":"this is my first note",
        }
        url= reverse("note:notes")
        header = {
            "HTTP_TOKEN":token,
        }
        response = client.post(url, notes_data, content_type='application/json' , **header)
        json_data = json.loads(response.content)
        id = json_data.get('data').get("note")[0].get("id")
        #deleting exsisting note
        delete_note_data = {
            "id":id
        }
        response = client.delete(url, delete_note_data, content_type='application/json', **header)
        assert response.status_code == 204
    
    def test_to_add_notes_when_details_are_not_provided(self, client):

        #creating a user
        user = User.objects.create_user("jayesh34","jay@mail.com","jay_password")
        user.is_verified = True
        user.save()
        #logging the user
        login_data = {
            "username":"jayesh34",
            "password":"jay_password",
        }
        url = reverse("user:login")
        response = client.post(url,login_data)
        json_data = json.loads(response.content)
        token = json_data.get('data').get("token")
        #adding notes
        notes_data = {}
        url= reverse("note:notes")
        header = {
            "HTTP_TOKEN":token,
        }
        response = client.post(url, notes_data , **header)
        assert response.status_code == 400

    def test_add_notes_when_user_token_is_not_provided(self, client):

        #creating a user
        user = User.objects.create_user("jayesh34","jay@mail.com","jay_password")
        user.is_verified = True
        user.save()
        #logging the user
        login_data = {
            "username":"jayesh34",
            "password":"jay_password",
        }
        url = reverse("user:login")
        response = client.post(url,login_data)
        json_data = json.loads(response.content)
        token = json_data.get('data').get("token")
        #adding notes
        notes_data = {
            "title":"This is my first note",
            "description":"this is my first note",
            "labels":["comic","sci-fi"]
        }
        url= reverse("note:notes")
        response = client.post(url, notes_data)
        assert response.status_code == 400

    def test_fetch_notes_of_user_which_does_not_have_any(self, client):

        #creating user
        user = User.objects.create_user("jayesh34","jay@mail.com","jay_password")
        user.is_verified = True
        user.save()
        #logging the user
        login_data = {
            "username":"jayesh34",
            "password":"jay_password",
        }
        url = reverse("user:login")
        response = client.post(url,login_data)
        json_data = json.loads(response.content)
        token = json_data.get('data').get("token")
        url= reverse("note:notes")
        header = {
            "HTTP_TOKEN":token,
        }
        #fetching the note added by user
        response = client.get(url, **header)
        assert response.status_code == 200

    def test_to_update_note_which_does_not_exists(self, client):

        #creating user
        user = User.objects.create_user("jayesh34","jay@mail.com","jay_password")
        user.is_verified = True
        user.save()
        #logging the user
        login_data = {
            "username":"jayesh34",
            "password":"jay_password",
        }
        url = reverse("user:login")
        response = client.post(url,login_data)
        json_data = json.loads(response.content)
        token = json_data.get('data').get("token")
        url= reverse("note:notes")
        header = {
            "HTTP_TOKEN":token,
        }
        updated_note_data = {
            "title":"This is my first note",
            "description":"this is my updated note",
            "id":10
        }
        response = client.put(url, updated_note_data, content_type='application/json', **header)
        assert response.status_code == 404

    def test_to_delete_note_which_does_not_exsists(self, client):

        #creating user
        user = User.objects.create_user("jayesh34","jay@mail.com","jay_password")
        user.is_verified = True
        user.save()
        #logging the user
        login_data = {
            "username":"jayesh34",
            "password":"jay_password",
        }
        url = reverse("user:login")
        response = client.post(url,login_data)
        json_data = json.loads(response.content)
        token = json_data.get('data').get("token")
        url= reverse("note:notes")
        header = {
            "HTTP_TOKEN":token,
        }
        #deleting exsisting note
        delete_note_data = {
            "id":2
        }
        response = client.delete(url, delete_note_data, content_type='application/json', **header)
        assert response.status_code == 404

    def test_to_create_label(self, client):

        #creating a user
        user = User.objects.create_user("jayesh34","jay@mail.com","jay_password")
        user.is_verified = True
        user.save()
        #logging the user
        login_data = {
            "username":"jayesh34",
            "password":"jay_password",
        }
        url = reverse("user:login")
        response = client.post(url,login_data)
        json_data = json.loads(response.content)
        token = json_data.get('data').get("token")
        #adding label
        label_data = {
            "label":"comic",
            "color":"red"
        }
        url= reverse("note:label")
        header = {
            "HTTP_TOKEN":token,
        }
        response = client.post(url, label_data, content_type='application/json' , **header)
        assert response.status_code == 201

    def test_to_update_label(self, client):

        #creating a user
        user = User.objects.create_user("jayesh34","jay@mail.com","jay_password")
        user.is_verified = True
        user.save()
        #logging the user
        login_data = {
            "username":"jayesh34",
            "password":"jay_password",
        }
        url = reverse("user:login")
        response = client.post(url,login_data)
        json_data = json.loads(response.content)
        token = json_data.get('data').get("token")
        #adding notes
        label_data = {
            "label":"comic",
            "color":"red"
        }
        url= reverse("note:label")
        header = {
            "HTTP_TOKEN":token,
        }
        response = client.post(url, label_data, content_type='application/json' , **header)
        json_data = json.loads(response.content)
        id = json_data.get("data").get("id")
        label_id = {
            "id":id,
            "label":"updated",
            "color":"updated"
            }
        response = client.put(url, label_id, content_type='application/json', **header)
        assert response.status_code == 202

    def test_to_delete_label(self, client):

        #creating a user
        user = User.objects.create_user("jayesh34","jay@mail.com","jay_password")
        user.is_verified = True
        user.save()
        #logging the user
        login_data = {
            "username":"jayesh34",
            "password":"jay_password",
        }
        url = reverse("user:login")
        response = client.post(url,login_data)
        json_data = json.loads(response.content)
        token = json_data.get('data').get("token")
        #adding notes
        label_data = {
            "label":"comic",
            "color":"red"
        }
        url= reverse("note:label")
        header = {
            "HTTP_TOKEN":token,
        }
        response = client.post(url, label_data, content_type='application/json' , **header)
        json_data = json.loads(response.content)
        id = json_data.get("data").get("id")
        label_id = {
            "id":id,
            }
        response = client.delete(url, label_id, content_type='application/json', **header)
        assert response.status_code == 204

    def test_to_add_collaboraters(self, client):

        #creating a user
        user = User.objects.create_user("jayesh34","jay@mail.com","jay_password")
        user.is_verified = True
        user.save()
        #logging the user
        login_data = {
            "username":"jayesh34",
            "password":"jay_password",
        }
        url = reverse("user:login")
        response = client.post(url,login_data)
        json_data = json.loads(response.content)
        token = json_data.get('data').get("token")
        #adding notes
        notes_data = {
            "title":"This is my first note",
            "description":"this is my first note"
        }
        url= reverse("note:notes")
        header = {
            "HTTP_TOKEN":token,
        }
        response = client.post(url, notes_data, content_type='application/json' , **header)
        json_data = json.loads(response.content)
        id = json_data.get("data").get("note")[0].get("id")
        collaboraters_data = {
            "id":id,
            "collaborators":[
                    "jayesh34"
                ]
        }
        url= reverse("note:collaborate")
        response = client.put(url, collaboraters_data, content_type='application/json' , **header)
        assert response.status_code == 201

    def test_to_delete_collaboraters(self, client):

        #creating a user
        user = User.objects.create_user("jayesh34","jay@mail.com","jay_password")
        user.is_verified = True
        user.save()
        #logging the user
        login_data = {
            "username":"jayesh34",
            "password":"jay_password",
        }
        url = reverse("user:login")
        response = client.post(url,login_data)
        json_data = json.loads(response.content)
        token = json_data.get('data').get("token")
        #adding notes
        notes_data = {
            "title":"This is my first note",
            "description":"this is my first note"
        }
        url= reverse("note:notes")
        header = {
            "HTTP_TOKEN":token,
        }
        response = client.post(url, notes_data, content_type='application/json' , **header)
        json_data = json.loads(response.content)
        id = json_data.get("data").get("note")[0].get("id")
        collaboraters_data = {
            "id":id,
            "collaborators":[
                    "jayesh34"
                ]
        }
        url= reverse("note:collaborate")
        response = client.put(url, collaboraters_data, content_type='application/json' , **header)
        note_data = {
            "id":id,
            "user":"jayesh34"
        }
        response = client.delete(url, note_data, content_type='application/json' , **header)
        assert response.status_code == 204

    def test_to_add_label_to_notes(self, client):

        #creating a user
        user = User.objects.create_user("jayesh34","jay@mail.com","jay_password")
        user.is_verified = True
        user.save()
        #logging the user
        login_data = {
            "username":"jayesh34",
            "password":"jay_password",
        }
        url = reverse("user:login")
        response = client.post(url,login_data)
        json_data = json.loads(response.content)
        token = json_data.get('data').get("token")
        #adding notes
        notes_data = {
            "title":"This is my first note",
            "description":"this is my first note"
        }
        url= reverse("note:notes")
        header = {
            "HTTP_TOKEN":token,
        }
        response = client.post(url, notes_data, content_type='application/json' , **header)
        json_data = json.loads(response.content)
        note_id = json_data.get("data").get("note")[0].get("id")
        #creating label
        label_data = {
            "label":"comic",
            "color":"red"
        }
        url= reverse("note:label")
        header = {
            "HTTP_TOKEN":token,
        }
        response = client.post(url, label_data, content_type='application/json' , **header)
        json_data = json.loads(response.content)
        label_id = json_data.get("data").get("id")
        note_data = {
            "id":note_id,
            "label":[label_id]
        }
        url= reverse("note:label_note")
        response = client.put(url, note_data, content_type='application/json' , **header)
        assert response.status_code == 201

    def test_to_delete_label_to_notes(self, client):

        #creating a user
        user = User.objects.create_user("jayesh34","jay@mail.com","jay_password")
        user.is_verified = True
        user.save()
        #logging the user
        login_data = {
            "username":"jayesh34",
            "password":"jay_password",
        }
        url = reverse("user:login")
        response = client.post(url,login_data)
        json_data = json.loads(response.content)
        token = json_data.get('data').get("token")
        #adding notes
        notes_data = {
            "title":"This is my first note",
            "description":"this is my first note"
        }
        url= reverse("note:notes")
        header = {
            "HTTP_TOKEN":token,
        }
        response = client.post(url, notes_data, content_type='application/json' , **header)
        json_data = json.loads(response.content)
        note_id = json_data.get("data").get("note")[0].get("id")
        #creating label
        label_data = {
            "label":"comic",
            "color":"red"
        }
        url= reverse("note:label")
        header = {
            "HTTP_TOKEN":token,
        }
        response = client.post(url, label_data, content_type='application/json' , **header)
        json_data = json.loads(response.content)
        label_id = json_data.get("data").get("id")
        note_data = {
            "id":note_id,
            "label_id":label_id
        }
        url= reverse("note:label_note")
        response = client.delete(url, note_data, content_type='application/json' , **header)
        assert response.status_code == 204

    def test_to_fetch_labes_added_by_particular_user(self,client):
        
        #creating a user
        user = User.objects.create_user("jayesh34","jay@mail.com","jay_password")
        user.is_verified = True
        user.save()
        #logging the user
        login_data = {
            "username":"jayesh34",
            "password":"jay_password",
        }
        url = reverse("user:login")
        response = client.post(url,login_data)
        json_data = json.loads(response.content)
        token = json_data.get('data').get("token")
        #adding notes
        notes_data = {
            "title":"This is my first note",
            "description":"this is my first note"
        }
        url= reverse("note:notes")
        header = {
            "HTTP_TOKEN":token,
        }
        response = client.post(url, notes_data, content_type='application/json' , **header)
        json_data = json.loads(response.content)
        note_id = json_data.get("data").get("note")[0].get("id")
        #creating label
        label_data = {
            "label":"comic",
            "color":"red"
        }
        url= reverse("note:label")
        response = client.post(url, label_data, content_type='application/json' , **header)
        json_data = json.loads(response.content)
        label_id = json_data.get("data").get("id")
        note_data = {
            "id":note_id,
            "label":[label_id]
        }
        url= reverse("note:label_note")
        response = client.put(url, note_data, content_type='application/json' , **header)
        url = reverse("note:user_label")
        print(url)
        response = client.get(url,**header)
        assert response.status_code == 202

    