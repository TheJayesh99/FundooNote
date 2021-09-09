from django.urls import path

from notes import views

urlpatterns = [
    path('',view= views.Notes.as_view(),name='notes'),
]
