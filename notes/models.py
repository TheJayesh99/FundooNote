from django.db import models
from user_api.models import User


# Create your models here.
class Labels(models.Model):

    label = models.CharField(max_length=10,default="")
    color = models.CharField(max_length=10,default="yellow")
    
class NotesModel(models.Model):

    """
    Notes model which will consist of 
    title as char field ,
    description as text field and 
    user id as foregin key
    label as list of labels for a notes
    """
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.ManyToManyField(Labels, related_name="labels",default=0)
    collaborators = models.ManyToManyField(User, related_name="collaborators",default=0)
    is_archive = models.BooleanField(default=False)
    is_binned = models.BooleanField(default=False)
