from django.shortcuts import render
from .forms import *
from django.db.models import Q
from django.http import HttpResponse
import json
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
    return render(request,'discuss/inside.html',context)
             
