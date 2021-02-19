from django.shortcuts import render
from .forms import *
from django.http import HttpResponseRedirect
# Create your views here.
def homepage(request):
    context = {}
    data = Articles.objects.all().order_by('date_Publish')
    context['carousel'] = data[:4]
    return render(request,'blogs/homepage.html',context)

def create(request):
    context = {}
    if request.method == 'POST':
        form = Article_form(request.POST,request.FILES)
        if form.is_valid():
            ins = form.save(commit = False)
            ins.user_name2 = request.user
            data = form.cleaned_data['content'] 
            title = form.cleaned_data['title'].lower().replace(" ","-")
            ins.link = f"/blog/{title}/{ins.id}/"
            if len(data) > 300:
                ins.description = data[:301]
            else:
                ins.description = data
            ins.save()
            return HttpResponseRedirect('/blog/')
        else:
            context['error'] = form.errors
    else:
        form = Article_form()
    context['form'] = form
    return render(request,'blogs/create.html',context)