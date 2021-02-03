from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
# Create your models here.
class Quora(models.Model):
    CHOICE = (
        ('General','General'),('Experience','Experience'),('Question','Question'),('Support','Support')
    )
    user = models.ForeignKey(User, related_name='Quora_User', to_field='username', on_delete=models.CASCADE,default="")
    title = RichTextUploadingField(unique = True,blank=True)
    title2 = models.CharField(max_length=10000,blank=True)
    tags = models.CharField(max_length=1000,blank=True)
    like = models.ManyToManyField(User,related_name="Quora_likes",blank=True)
    dislike = models.ManyToManyField(User,related_name="Quora_dislikes",blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    anonymous = models.BooleanField(default = False)
    category = models.CharField(max_length=1000,choices = CHOICE,default="General")
    pinned = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)



class Anwsers(models.Model):
    instance = models.ForeignKey(Quora,related_name="Quora_anwsers",to_field="title",on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='Anwser_User', to_field='username', on_delete=models.CASCADE,default="")
    anwser = RichTextUploadingField()
    like = models.ManyToManyField(User,related_name="anwser_like")
    dislike = models.ManyToManyField(User,related_name="anwser_dislike")
    created = models.DateTimeField(auto_now_add=True,null=True)
    anonymous = models.BooleanField(default = False)
    pinned = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return self.user.username


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comment_user', to_field='username', on_delete=models.CASCADE,default="")
    question = models.ForeignKey(Quora, related_name='quora_comment',on_delete=models.CASCADE,default="")
    post = models.ForeignKey(Anwsers, related_name='Anwser_comment',on_delete=models.CASCADE)
    parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE,related_name="replies_name")
    body = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True,null=True)
    active = models.BooleanField(default=True)
    like = models.ManyToManyField(User,related_name="comment_like")
    dislike = models.ManyToManyField(User,related_name="comment_dislike")
    class Meta:
        ordering = ('-created',)
    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
    @property
    def sorting(self):
        return Comment.objects.filter(parent = self).order_by("created")
    def __str__(self):
        return self.body



class QuoraComment(models.Model):
    user = models.ForeignKey(User, related_name='quora_comment_user', to_field='username', on_delete=models.CASCADE,default="")
    question = models.ForeignKey(Quora, related_name='quora_comment_ques',on_delete=models.CASCADE,default="")
   
    parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE,related_name="quora_replies_name")
    body = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True,null=True)
    active = models.BooleanField(default=True)
    like = models.ManyToManyField(User,related_name="quora_comment_like")
    dislike = models.ManyToManyField(User,related_name="quora_comment_dislike")
    class Meta:
        ordering = ('-created',)
    def children(self):
        return QuoraComment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
    @property
    def sorting(self):
        return QuoraComment.objects.filter(parent = self).order_by("created")
    def __str__(self):
        return self.body


