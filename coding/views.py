from django.shortcuts import render
from datetime import date
from .models import *

# Create your views here.
def homepage(request):
    context = {}
    context['day'] = date.today()
    solved = 0
    easy = 0
    medium = 0
    hard = 0
    attempted = 0
    ques = []
    todo = 0
    total = 0
    for i in Programming.objects.all():
        total +=1
        ques.append(i)
        if i.status == 'Solved':
            solved+=1
            if i.difficulty == 'Easy':
                easy +=1
            elif i.difficulty == 'Moderate':
                medium +=1
            else:
                hard +=1
        elif i.status == 'Attempted':
            attempted +=1
        else:
            todo +=1
    data = {
        'ques' : ques,
        'solved' : solved,
        'Easy' : easy,
        'Medium' : medium,
        'Hard' : hard,
        'Attempted' : attempted,
        'todo' : todo,
        'total' : total
    }


    context['data'] = data
    context['category'] = Programming_Category.objects.all().order_by('category_name')
    context['companies'] = Programming_Companies.objects.all().order_by('company_name')
    return render(request,'coding/homepage.html',context)

def inside(request,title,ins):
    return render(request,'coding/inside.html')
