from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.
class Language(models.Model):
    lang = models.CharField(max_length=1000,unique = True)
    template = models.TextField(blank = True)
    def __str__(self):
        return self.lang

class PlayGround(models.Model):
    CHOICE = (
        ('Console','Console'),('Frontend','Frontend'),
    )
    user = models.ForeignKey(User, related_name='playground_user', to_field='username', on_delete=models.CASCADE)
    title = models.CharField(max_length=1000,blank = False,default="Untitled")
    category = models.CharField(max_length=1000,choices = CHOICE,default="Console" )
    link = models.TextField(blank = True)
    embed = models.TextField(blank=True)
    live = models.BooleanField(default=False)
    def __str__(self):
        return self.title + str(self.user) 

class ExtendPlay(models.Model):
    instance = models.ForeignKey(PlayGround, related_name='playground_ins', on_delete=models.CASCADE)
    lang = models.ForeignKey(Language, related_name='playground_lang', to_field='lang', on_delete=models.CASCADE)
    code = models.TextField(blank = True,null = True)
    def __str__(self):
        return str(self.instance.id)

class Libraries(models.Model):
    template = models.CharField(max_length=1000,unique = True)
    def __str__(self):
        return self.template
class Frontend(models.Model):
    CHOICE = (
        ('HTML','HTML'),('CSS','CSS'),('JavaScript','JavaScript'),('SCSS','SCSS')
    )
    method = models.ForeignKey(Libraries,related_name="Frontend_libraries",on_delete=models.CASCADE,to_field="template")
    language = models.CharField(max_length=1000,choices=CHOICE,default="HTML")
    html = models.TextField(blank=True)
    css = models.TextField(blank=True)
    js = models.TextField(blank=True)
    scss = models.TextField(blank=True)
    def __str__(self):
        return self.method.template

    class Meta:
        unique_together = ('method','language')

class ExtendFrontend(models.Model):
    instance = models.ForeignKey(PlayGround, related_name='playground_frontend', on_delete=models.CASCADE)
    html = models.TextField(blank=True)
    css = models.TextField(blank=True)
    js = models.TextField(blank=True)
    scss = models.TextField(blank=True)
    def __str__(self):
        return str(self.instance.id)




