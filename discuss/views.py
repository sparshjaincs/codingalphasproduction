from django.shortcuts import render
from .forms import *
from django.db.models import Q
from django.http import HttpResponse
import json
from .models import *
# Create your views here.
def homepage(request):
    context = {}
    method = request.GET.get('method')
    if method is None or method == "":
        method = 'General'
    context['method'] = method
    if method == 'General':
        quora = Quora_Form()
    else:
        quora = Other_Form
    context['form'] = quora
    context['pinned'] = Quora.objects.filter(category=method,pinned=True).order_by('-created')
    context['data'] = Quora.objects.filter(~ Q(id__in = Quora.objects.filter(category=method,pinned=True)),category=method).order_by('-created')[:20]
    return render(request,'discuss/homepage.html',context)

def quora_submit(request):
    if request.method == 'POST':
        method  = request.POST.get('method')
        temp = request.POST.get('title')
        tags = request.POST.get('tags')
        anonymous = request.POST.get('anonymous')
        if anonymous == "1":
            anonymous = True
        else:
            anonymous = False
        if method == 'General':
            if temp is None or temp == "":
                return HttpResponse(json.dumps(["error","Question Field Can't be empty."]))
            else:
                try:
                    ins = Quora(user=request.user,title=temp,tags=tags.strip(),anonymous = anonymous,category=method)
                    ins.save()
                    data = {
                        
                        
                        'status':'You successfully submited your question.',
                    }
                    return HttpResponse(json.dumps(data))

                except Exception as exp:
                    return HttpResponse(json.dumps(['error','Question Already Exists']))
        else:
            title2 = request.POST.get('title2')
            if title2 is None or title2 == "":
                return HttpResponse(json.dumps(["error","Title Field Can't be empty."]))
            elif temp is None or temp == "":
                return HttpResponse(json.dumps(["error","Question Field Can't be empty."]))
            else:
                try:
                    ins = Quora(user=request.user,title=temp,title2 = title2, tags=tags.strip(),anonymous = anonymous,category=method)
                    ins.save()
                    data = {
                        
                        
                        'status':'You successfully submited your question.',
                    }
                    return HttpResponse(json.dumps(data))

                except Exception as exp:
                    return HttpResponse(json.dumps(['error','Question Already Exists.']))


def inside(request,method,id):
    context = {}
    context['method'] = method
    ins =  Quora.objects.get(id = id)
    context['data'] =ins
    context['like'] = True if request.user in ins.like.all() else False
    context['dislike'] = True if request.user in ins.dislike.all() else False
    if method == 'General':
        form = Anwser_Form()
        context['form'] = form
        

    return render(request,'discuss/inside.html',context)

def anwser_submit(request):
    if request.method == 'POST':
        temp = request.POST.get('title')
        anonymous = request.POST.get('anonymous')
        ins = request.POST.get('id')
        if anonymous == "1":
            anonymous = True
        else:
            anonymous = False
        if temp is None or temp == "":
            return HttpResponse(json.dumps(["error","Anwser Field Can't be empty."]))
        else:
            try:
                    ins = Anwsers( instance = Quora.objects.get(id = ins), user=request.user,anwser = temp,anonymous = anonymous)
                    ins.save()
                    data = {
                        
                        
                        'status':'You successfully submited your question.',
                    }
                    return HttpResponse(json.dumps(data))

            except Exception as exp:
                    print(exp)
                    return HttpResponse(json.dumps(['error','Question Already Exists.']))
        
def comment_submit(request):
    if request.method == 'POST':
        method = request.POST.get('method')
        ty  = request.POST.get('type')
        questionid  = request.POST.get('id')
        anwserid  = request.POST.get('anwserid')
        body  = request.POST.get('body')
        proper = request.POST.get('property')
        commentid = request.POST.get('commentid')
        inputid = request.POST.get('inputid')
        if method == 'discuss':
            if ty == 'General':
                if body is None or body == '':
                    return HttpResponse(json.dumps(['error',"Comment Field Can't be empty!"]))
                else:
                    try:
                        if proper == 'reply' or proper == 'reply1' or proper == 'reply2':
                            
                            comm = Comment.objects.get(id = commentid)
                            if inputid:
                                ref = inputid
                            else:
                                ref = comm.id
                            name = f"<a href='#reference{ref}' onclick='blink("+f'"reference{ref}"'+")'>@"+comm.user.profile.first_name + " " + comm.user.profile.last_name+"</a> "
                            ins = Comment(user = request.user,question = Quora.objects.get(id = questionid),post = Anwsers.objects.get(id = anwserid),body =name + body,parent = comm)
                        else:
                            ins = Comment(user = request.user,question = Quora.objects.get(id = questionid),post = Anwsers.objects.get(id = anwserid),body = body)
                        ins.save()
                        data = {
                            'user':ins.user.username,
                            'name':ins.user.profile.first_name + " " + ins.user.profile.last_name,
                            'id':ins.id,
                            'body':ins.body,
                            'profile':str(ins.user.profile.avatar),
                            'time':str(ins.created.strftime("%B. %d, %m %H:%M %p")),
                            'replies':Comment.objects.filter(parent = ins).count(),

                        }
                        return HttpResponse(json.dumps(['success',data]))
                        
                    except Exception as exp:
                        return HttpResponse(json.dumps(['error',str(exp)]))

             
