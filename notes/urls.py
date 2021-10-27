from django.urls import path

from notes import views

app_name="note"
urlpatterns = [
    path('',view= views.Notes.as_view(),name='notes'),
    path('label/',view= views.Label.as_view(),name='label'),
    path('label/<int:id>',view= views.Label.as_view(),name='label'),
    path('collaboraters/',view= views.Collaborators.as_view(),name='collaborate'),
    path('noteLabel/',view= views.LabelNote.as_view(),name='label_note'),
    path('noteLabel/<int:id>',view= views.LabelNote.as_view(),name='label_note'),
    path('userLabels/',view= views.UserLabel.as_view(),name='user_label'),
]
