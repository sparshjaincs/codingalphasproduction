from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
class Note(models.Model):
    username = models.ForeignKey(User, related_name='notebookuser', to_field='username', on_delete=models.CASCADE)
    heading = models.CharField(max_length = 1000,blank=False,default="")
    desciption = RichTextField(blank = True)
    text = RichTextField(blank = True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username.username

    class Meta:
        ordering = ['-created']