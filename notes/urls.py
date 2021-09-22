from django.urls import path

from notes import views

app_name="note"
urlpatterns = [
    path('',view= views.Notes.as_view(),name='notes'),
    path('label/',view= views.Label.as_view(),name='label'),
]
