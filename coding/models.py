from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
class Language(models.Model):
    lang = models.CharField(max_length=1000,unique = True)
    template = models.TextField(blank = True)
    def __str__(self):
        return self.lang
class Programming_Companies(models.Model):
    company_name = models.CharField(max_length=1000,unique = True)
    def __str__(self):
        return self.company_name
class Programming_Category(models.Model):
    category_name = models.CharField(max_length=1000,unique = True)
    def __str__(self):
        return self.category_name
class Programming(models.Model):
    FIELD = (
        ('Easy','Easy'),
        ('Moderate','Moderate'),('Hard',"Hard"),
    )
    CHOICES = (
        ('Todo','Todo'),('Solved','Solved'),('Attempted','Attempted'),
    )
    video_choice = (
        ('Has solution','Has solution'),
        ('Has video solution','Has video solution'),
    )
    title = models.CharField(max_length=1000,unique = True)
    description = RichTextField(blank = True)
    solution = RichTextField(blank=True)

    difficulty = models.CharField(max_length=100,choices = FIELD,default="Easy")
    tags = models.ManyToManyField(Programming_Category,default=None,blank=True,related_name="program_tags")
    status = models.CharField(max_length=1000,choices = CHOICES,default="Todo")
    like = models.ManyToManyField(User,default=None,blank=True,related_name="program_likes")
    dislike = models.ManyToManyField(User,default=None,blank=True,related_name="program_dislikes")
    company = models.ManyToManyField(Programming_Companies,default=None,blank=True,related_name="program_company")
    video = models.CharField(max_length=1000,choices = video_choice,default="Has solution")
    category = models.ForeignKey(Programming_Category,related_name="program_category",to_field="category_name",on_delete=models.CASCADE,default="Arrays")
    def __str__(self):
        return self.title
class Templates(models.Model):
    instance = models.ForeignKey(Programming,related_name="temlate_ques",to_field="title",on_delete=models.CASCADE)
    language = models.ForeignKey(Language,related_name="temp_lang_name",to_field="lang",on_delete=models.CASCADE)
    temp = models.TextField(blank = False)
    code = models.TextField(blank = True)
    snippet = models.TextField(blank = True)
    solution = models.TextField(blank = True)
    def __str__(self):
        return str(self.instance) + str(self.language)

class TestCase(models.Model):
    instance = models.ForeignKey(Programming,related_name="testcase_ques",to_field="title",on_delete=models.CASCADE)
    cases = models.TextField(blank = False)
    sol_cases = models.TextField(blank= False)
    public_cases = models.TextField(blank=False)
    public_sol_cases = models.TextField(blank = False)

    def __str__(self):
        return str(self.instance)
    

class Solution(models.Model):
    program = models.ForeignKey(Programming,related_name="question_sol",to_field="title",on_delete=models.CASCADE)
    title = models.CharField(max_length=1000,unique = True)
    solution = RichTextField(blank=True)
    video = models.TextField(blank = True)
    def __str__(self):
        return str(self.title)

class Code_Snippet(models.Model):
    program = models.ForeignKey(Programming,related_name="code_sol",to_field="title",on_delete=models.CASCADE,default="Longest Palindromic Substring")
    solution = models.ForeignKey(Solution,related_name="Sol_Snippet",to_field="title",on_delete=models.CASCADE)
    language = models.ForeignKey(Language,related_name="language_name",to_field="lang",on_delete=models.CASCADE)
    code = models.TextField(blank = True)
    def __str__(self):
        return str(self.solution)

class Todo(models.Model):
    username = models.ForeignKey(User,related_name="todo_user",to_field="username",on_delete=models.CASCADE)
    title = models.CharField(max_length=1000,blank = False,default="Untitled")
    question = models.ManyToManyField(Programming,related_name="todo_question",default=None,blank = True)
    def __str__(self):
        return str(self.username)

class Submission(models.Model):
    CHOICES = (
        ('Accepted','Accepted'),('Wrong Anwser','Wrong Anwser'),('Runtime Error','Runtime Error'),
    )
    username = models.ForeignKey(User,related_name="submission_user",to_field="username",on_delete=models.CASCADE)
    question =  models.ForeignKey(Programming,related_name="submission_question",to_field="title",on_delete=models.CASCADE)
    status = models.CharField(max_length=1000,choices = CHOICES)
    language = models.ForeignKey(Language,related_name="submission_lang",to_field="lang",on_delete=models.CASCADE)
    runtime = models.IntegerField(default = 0)
    time = models.DateField(default=datetime.now)
    solution = models.TextField(default = "")
    def __str__(self):
        return str(self.question)
    
    







    
