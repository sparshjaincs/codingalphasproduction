from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from discuss.models import Quora
from discuss.models import Anwsers as AnsModel
from Core.models import *
from .forms import *
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import login, authenticate
from django.contrib import messages
class MyPasswordResetView(UserPassesTestMixin, PasswordResetView):
    template_name = 'Core/snippets/password_reset.html'

    # https://docs.djangoproject.com/en/2.2/ref/contrib/auth/#django.contrib.auth.models.User.is_anonymous
    def test_func(self):
        return self.request.user.is_anonymous  

# Create your views here.

def create(request):
    context = {}
    if(request.method == 'POST'):
        form = SignUpForm(request.POST) # fill it with user details
        if form.is_valid():
            user = form.save(commit = False)

            username = form.cleaned_data.get('email').split('@')[0]
            user.username = username
            user.save()
            ins = Profile.objects.get(user = user)
            ins.first_name = form.cleaned_data.get('first_name')
            ins.last_name = form.cleaned_data.get('last_name')
            ins.email = form.cleaned_data.get('email')
            ins.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.error(request,str(form.errors))
    context['form'] = SignUpForm()
    return render(request,'Core/snippets/createAccount.html',context)

def homepage(request):
    if request.user.is_authenticated:
        return render(request,"Core/homepage.html")
    else:
        return render(request,"Core/frontend.html")

def like(request):
    method = request.GET.get('method')
    instance = request.GET.get('instance')
    if method == 'discuss':
        ins = Quora.objects.get(id = instance)
        if request.user in ins.like.all():
            ins.like.remove(request.user)
            status = 0
        else:
            ins.like.add(request.user)
            if request.user in ins.dislike.all():
                ins.dislike.remove(request.user)
            status = 1
        likecount = ins.like.all().count()  
        dislikecount = ins.dislike.all().count()
    elif method == 'discussanwser':
        ins = AnsModel.objects.get(id=instance)
        if request.user in ins.like.all():
            ins.like.remove(request.user)
            status = 0
        else:
            ins.like.add(request.user)
            if request.user in ins.dislike.all():
                ins.dislike.remove(request.user)
            status = 1  
        likecount = ins.like.all().count()  
        dislikecount = ins.dislike.all().count()

    return HttpResponse(json.dumps([status,likecount,dislikecount]))


def dislike(request):
    method = request.GET.get('method')
    instance = request.GET.get('instance')
    if method == 'discuss':
        ins = Quora.objects.get(id = instance)
        if request.user in ins.dislike.all():
            ins.dislike.remove(request.user)
            status = 0
        else:
            ins.dislike.add(request.user)
            if request.user in ins.like.all():
                ins.like.remove(request.user)
            status = 1
        dislikecount = ins.dislike.all().count()
        likecount = ins.like.all().count() 
    elif method == 'discussanwser':
        ins = AnsModel.objects.get(id = instance)
        if request.user in ins.dislike.all():
            ins.dislike.remove(request.user)
            status = 0
        else:
            ins.dislike.add(request.user)
            if request.user in ins.like.all():
                ins.like.remove(request.user)
            status = 1
        dislikecount = ins.dislike.all().count()
        likecount = ins.like.all().count() 
    return HttpResponse(json.dumps([status,dislikecount,likecount]))


def follow(request):
    us = request.GET.get('method')
    ins = User.objects.get(username = us)
    if request.user in ins.profile.following.all():
        ins.profile.following.remove(request.user)
        status = 0
    else:
        ins.profile.following.add(request.user)
        status = 1
    if ins in request.user.profile.follow.all():
        request.user.profile.follow.remove(request.user)
    else:
        request.user.profile.follow.add(request.user)
    return HttpResponse(json.dumps([status]))

def mark(request):
    method = request.GET.get('method')
    ins = request.GET.get('ins')
    if method == 'discuss':
        instance = Profile.objects.get(user = request.user)
        ins = Quora.objects.get(id = ins)
        if ins in instance.quora_discuss.all():
            instance.quora_discuss.remove(ins)
            status = 0
        else:
            instance.quora_discuss.add(ins)
            status = 1
    

    return HttpResponse(json.dumps([status]))


