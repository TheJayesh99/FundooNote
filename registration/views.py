from django.shortcuts import HttpResponse
from .models import Registration
# Create your views here.
def registration(request):

    """
    Method to get data from the user and set them in data base
    """
    if request.method == 'POST':
        username = request.POST["username"]
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        password = request.POST['password']
        try:
            register_user = Registration(username= username,first_name= first_name,last_name= last_name,phone_number= phone_number,email= email,password=password)
            register_user.save()
            return HttpResponse(f"Registered with username {username}")
        except Exception as e:
            return HttpResponse(f"Registration Failed")
    return HttpResponse(f"Welcome to registration plz register")