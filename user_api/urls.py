from django.urls import path
from user_api import views

urlpatterns = [
    path("register/",view=views.Register.as_view(),name="register"),
    path("login/",view=views.Login.as_view(),name="login"),
    path("verify/<str:token>/",view= views.Verification.as_view(),name="Verification")
]
