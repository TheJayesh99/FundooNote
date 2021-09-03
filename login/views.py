from django.shortcuts import HttpResponse
from registration.models import Registration

# Create your views here.
def login(request):

    """
    Method to validate the given username and password
    """
    if request.method == "POST":
        try:
            check_user = Registration.objects.get(username=request.POST["username"])
            if check_user.password == request.POST["password"]:
                return HttpResponse("Logined successfully")
            return HttpResponse("Password MissMatched")
        except Exception as e:
            return HttpResponse("No such user Found")
    return HttpResponse("Welcome to login page")