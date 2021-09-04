from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
# Create your views here.
def registration(request):

    """
    Method to get data from the user and set them in data base
    """
    if request.method == 'POST':
        try:
            username = request.POST["username"]
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            #creating a user model
            new_user = User.objects.create_user(username, email, password)
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.save()
            return HttpResponse(f"Registered with username {username}")
        except Exception as e:
            return HttpResponse(f"Registration Failed")
    return HttpResponse(f"Welcome to registration plz register")