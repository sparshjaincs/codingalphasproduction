from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
#from .views import current_user as cu
# Create your models here.

class Categories(models.Model):
    CHOICES = (('All','All'),
		('Quants', 'Quants'),('Verbal', 'Verbal'),('Logical','Logical'))
    choice = models.CharField(max_length=1000,choices=CHOICES,default="All")
    category_name = models.CharField(max_length=40, unique=True)
    def __str__(self):
        return self.category_name


class Articles(models.Model):
    STATUS_CHOICES = (
		('draft', 'Draft'),('published', 'Published'),)
    METHOD_CHOICES = (
		('blog', 'blog'),('design', 'design'),('editor','editor'),('learn','learn'))
    user_name2 = models.ForeignKey(User, related_name='project_username_2', to_field='username', on_delete=models.CASCADE)
    title = RichTextField(default=" ",blank=False,unique=True)
    project_name = models.CharField(max_length=100, blank=False , null=False)
    author = models.CharField(max_length=50,blank=True)
    date_Publish = models.DateField(default=datetime.now)
    date_updated = models.DateField(default=datetime.now)
    category = models.ForeignKey(Categories,related_name = 'category', to_field='category_name',on_delete=models.CASCADE,default=" ")
    image = models.ImageField(upload_to='users/images',blank=True,default='',null=True)
    video= models.FileField(upload_to='users/video', null=True,blank=True ,verbose_name="Video")
    image2 = models.CharField(max_length=1000,blank=True,null=True)
    content = RichTextField(blank=False,null=True)
    link = models.TextField(blank=True,default="")
    description = models.TextField(blank=True,default="")
    time= models.TimeField(blank=False,default=datetime.now())
    tags = models.CharField(max_length=300,blank=False,default="",null=True,help_text='Add comma( ,) seperated tags!!')
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='published')
    method=models.CharField(max_length=10,choices=METHOD_CHOICES,default='blog')
    liked = models.ManyToManyField(User,default=None,blank=True,related_name="likes_title")
    disliked = models.ManyToManyField(User,default=None,blank=True,related_name="dislikes_title")
    
   
    template = models.CharField(max_length=1000,blank=True,null=True)
    quora = models.CharField(max_length=1000,blank=True,null=True)
    medium= models.CharField(max_length=1000,blank=True,null=True)
    facebook = models.CharField(max_length=1000,blank=True,null=True)
    instagram = models.CharField(max_length=1000,blank=True,null=True)
    twitter = models.CharField(max_length=1000,blank=True,null=True)
    other= models.CharField(max_length=1000,blank=True,null=True)

    question_field =  models.BooleanField(default=False)
    
    
	
   
    class Meta:
        ordering = ('date_Publish','time')
    def __str__(self):
        return self.title
    @property
    def num_likes(self):
        return self.liked.all().count()

    @property
    def num_dislikes(self):
        return self.disliked.all().count()

    
class Anwsers(models.Model):
    user_anwser = models.ForeignKey(User, related_name='user_anwser_1', to_field='username', on_delete=models.CASCADE)
    question = models.ForeignKey(Articles, related_name='user_question_4', to_field='title', on_delete=models.CASCADE)
    time= models.TimeField(blank=False,default=datetime.now())
    date = models.DateField(default=datetime.now)
    description = models.TextField(blank=True,default="")
    explanation = RichTextField(blank=False,null=True)
    class Meta:
        ordering = ('-date','-time')
    def __str__(self):
        return str(self.question)


class Discussion_comment(models.Model):
    user_discussion = models.ForeignKey(User, related_name='user_discussion_1', to_field='username', on_delete=models.CASCADE,default="")
    post = models.ForeignKey(Anwsers, related_name='discussion',on_delete=models.CASCADE)
    parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE)
    body = models.CharField(max_length=100000,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('-created',)
    def children(self):
        return Discussion_comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
    def __str__(self):
        return self.post.question.title


 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True,default="")
    last_name = models.CharField(max_length=50, blank=True,default="")
    email = models.EmailField(max_length=50, blank=True,default="")
    phone_number = models.CharField(max_length=13, blank=True,default="")
    avatar = models.ImageField(upload_to='users/images',blank=False,default = 'users/images/default.jpg')
    headline = models.CharField(max_length=1000, blank=True,default="")
    bio = models.TextField(blank=True,default="")
    address = models.CharField(max_length=50, blank=True,default="")
    city = models.CharField(max_length=50, blank=True,default="")
    state  = models.CharField(max_length=50, blank=True,default="")
    country = models.CharField(max_length=50, blank=True,default="")
    date_of_birth = models.CharField(max_length=13, blank=True,default="")
    follow = models.ManyToManyField(User,default=None,blank=True,related_name="follow_title")
    following = models.ManyToManyField(User,default=None,blank=True,related_name="following_title")
    signup_confirmation = models.BooleanField(default=False)
    instagram = models.CharField(max_length=1000,blank=True,null=True)
    facebook = models.CharField(max_length=1000,blank=True,null=True)
    twitter = models.CharField(max_length=1000,blank=True,null=True)
    college = models.CharField(max_length=1000, blank=True,default="")
    medium = models.CharField(max_length=1000,blank=True,null=True)
    quora = models.CharField(max_length=1000,blank=True,null=True)
    other = models.CharField(max_length=1000,blank=True,null=True)
    favourities = models.ManyToManyField(Articles,blank=True,related_name="articles_titles")

    subscribe = models.ManyToManyField(User,default=None,blank=True,related_name="subscribe_title")
    mute = models.ManyToManyField(User,default=None,blank=True,related_name="mute_title")
    
  
    

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class my_comment(models.Model):
    post = models.ForeignKey(Articles, related_name='my_comments',on_delete=models.CASCADE)
    parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True,null=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('-created',)
    def children(self):
        return my_comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)

    

class activity(models.Model):
    CHOICE = (
        ('User','User'),
    )
    user_name3 = models.ForeignKey(User, related_name='project_username_3', to_field='username', on_delete=models.CASCADE)
    user_activity = models.CharField(max_length=200,blank=True)
    activity_icon = models.CharField(max_length=200,blank=True)
    category = models.CharField(max_length=1000,choices=CHOICE,default="User")
    activity_time= models.TimeField(blank=False,default=datetime.now())
    color =  models.CharField(blank=False,default="text-info",max_length=100)
    date_activity = models.DateField(default=datetime.now)
    activity_count = models.IntegerField(default =0,null=True)
    def __str__(self):
        return f'{self.user_name3}  -- > Activty {self.user_activity}'
class Notifications(models.Model):
      user_name4 = models.ForeignKey(User,related_name="user_name4_notification",to_field='username',on_delete=models.CASCADE)
      activity_count = models.IntegerField(default =0)
    
      activity_profile_count = models.IntegerField(default =0)
     
      follow_count = models.IntegerField(default =0)
      following_count = models.IntegerField(default =0)
      def __str__(self):
          return " activity_count "+ str(self.activity_count) + " follow_count " + str(self.follow_count)+ " following_count " + str(self.following_count)

class titleview(models.Model):
    view = models.ForeignKey(Articles,related_name="titleview",to_field='id',on_delete=models.CASCADE)
    ip_addr = models.CharField(max_length=300,blank=True,null=True)
    def __str__(self):
        return str(self.view)+ " " + str(self.ip_addr)



class Topic(models.Model):
    CHOICES = (('All','All'),
		('Quants', 'Quants'),('Verbal', 'Verbal'),('Logical','Logical'))
    choice = models.ForeignKey(Categories,related_name="catview",to_field='category_name',on_delete=models.CASCADE,default="All")
    topic_name = models.CharField(max_length=40, unique=True,default="")
    def __str__(self):
        return self.topic_name

class Company(models.Model):
    company_name = models.CharField(max_length=100, unique=True,default="")
    def __str__(self): 
        return self.company_name

class Syllabus(models.Model):
    name = models.ForeignKey(Company,related_name="companies",to_field='company_name',on_delete=models.CASCADE)
    side_data = models.TextField(blank=False,null=True)
    pattern = RichTextField(blank=True,null=True)
    syll = RichTextField(blank=True,null=True)
    experience = RichTextField(blank=True,null=True)
    def __str__(self):
        return self.name.company_name 


class Aptitude(models.Model):
    question_id = models.AutoField(primary_key=True)
    STATUS_CHOICES = (
		('A', 'A'),('B', 'B'),('C', 'C'),('D', 'D'))
    DIFF_CHOICES = (
		('Easy', 'Easy'),('Medium', 'Medium'),('Hard', 'Hard'))
    question = RichTextUploadingField()
    A = models.TextField(blank=True,default="")
    B = models.TextField(blank=True,default="")
    C = models.TextField(blank=True,default="")

    D = models.TextField(blank=True,default="")
    E = models.TextField(blank=True,default="",null=True)
    
    correct = models.CharField(max_length=10,choices=STATUS_CHOICES)
    topic = models.ForeignKey(Topic,related_name="topicname",to_field='topic_name',on_delete=models.CASCADE)
    category = models.ForeignKey(Categories,related_name="categoryname1",to_field='category_name',on_delete=models.CASCADE,default="Quants")
    company = models.ForeignKey(Company,related_name="companyname",to_field='company_name',on_delete=models.CASCADE,default="Accenture")
    difficulty = models.CharField(max_length=10,choices=DIFF_CHOICES)
    time= models.TimeField(blank=False,default=datetime.now())
    date_Publish = models.DateField(default=datetime.now)

    exam_name = models.CharField(max_length=1000,null = True,blank=True)
    explanation = models.TextField(blank=True,default="")
    
    def __str__(self):
        return self.question


class List(models.Model):
    description =  models.TextField(blank=True,default="")
    heading =  models.TextField(blank=True,default="")
    link =  models.TextField(blank=True,default="")
    time= models.TimeField(blank=False,default=datetime.now())
    date = models.DateField(default=datetime.now)
    def __str__(self):
        return self.heading

class Job_Search(models.Model):
    user = models.ForeignKey(User,related_name="User_Jobs",to_field="username",on_delete=models.CASCADE)
    title = models.CharField(max_length=1000,blank = True)
    location = models.CharField(max_length=1000,blank = True)
    def __str__(self):
        return str(self.user)

    class Meta:
        unique_together = ('title','location')

class Module(models.Model):
    CHOICES = (
        ('All','All'),
        ('Free','Free'),
        ('Paid','Paid')
    )
    title = models.CharField(max_length = 1000,blank=False,unique = True)
    topic = models.ForeignKey(Topic,to_field="topic_name",related_name="Module_Topic",on_delete=models.CASCADE)
    category = models.ForeignKey(Categories,to_field="category_name",related_name="Module_Category",on_delete=models.CASCADE)
    status = models.CharField(max_length=1000,choices=CHOICES,default='All')
    question = models.ManyToManyField(Aptitude,related_name="Module_Question")
    company = models.ForeignKey(Company,to_field="company_name",related_name="Module_Companies",on_delete = models.CASCADE,default="")
    def __str__(self):
        return str(self.company) + " " + self.title + " " + self.status + " " + str(self.topic)





 