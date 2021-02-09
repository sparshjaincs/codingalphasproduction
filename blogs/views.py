from django.shortcuts import render
from .forms import *
# Create your views here.
def homepage(request):
    return render(request,'blogs/homepage.html')

def create(request):
    context = {}
    if request.method == 'POST':
        form = Article_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
        else:
            context['error'] = form.errors
    else:
        form = Article_form()
    context['form'] = form
    return render(request,'blogs/create.html',context)