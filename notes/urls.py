from django.urls import path

from notes import views

app_name="note"
urlpatterns = [
    path('',view= views.Notes.as_view(),name='notes'),
]
