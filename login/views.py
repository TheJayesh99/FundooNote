from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate

# Create your views here.
def login(request):

    """
    Method to validate the given username and password
    """
    if request.method == "POST":
        try:
            username=request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username,password=password)
            if user is not None:
                return HttpResponse(f"Logged In SuccesFully with {user.username}")
            return HttpResponse("Password MissMatched")
        except Exception as e:
            return HttpResponse("No such user Found")
    return HttpResponse("Welcome to login page")