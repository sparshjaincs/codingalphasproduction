from django.db import models
from coding.models import *
# Create your models here.
class DailyContest(models.Model):
    title = models.CharField(max_length = 1000,unique = True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.title

class ContestChapter(models.Model):
    instance = models.ForeignKey(DailyContest,related_name="contestchapters",to_field="title",on_delete=models.CASCADE)
    title = models.CharField(max_length = 1000,unique = True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.title

class ContestContent(models.Model):
    instance = models.ForeignKey(DailyContest,related_name="contestcontent",to_field="title",on_delete=models.CASCADE)
    chapter_instance = models.ForeignKey(ContestChapter,related_name="chaptercontent",to_field="title",on_delete=models.CASCADE)
    #title = models.CharField(max_length = 1000,unique = True)
    question = models.ForeignKey(Programming,related_name="contentquestion",to_field="title",on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.question.title
    



