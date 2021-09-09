from django.db import models
from user_api.models import User


# Create your models here.
class NotesModel(models.Model):

    """
    Notes model which will consist of 
    title as char field ,
    description as text field and 
    user id as foregin key
    """
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
