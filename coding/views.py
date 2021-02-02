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
    context = {}
    context['id'] = ins
    context['language'] = Language.objects.all()
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


    context['problem'] = data
    context['category'] = Programming_Category.objects.all().order_by('category_name')
    context['data'] =  Programming.objects.get(id = ins)
    return render(request,'coding/inside.html',context)



def filter(request):
    context = {}
    method = request.GET.get('method')
    value = request.GET.get('value')
    if method == 'tags':
        instance = Programming.objects.filter(tags = Programming_Category.objects.get(category_name = value))
  
   
    elif method == 'company':
        instance = Programming.objects.filter(company = Programming_Companies.objects.get(company_name = value))
    elif method == 'All':
        instance = Programming.objects.all()
    elif method == 'status':
        instance = Programming.objects.filter(status = value)
    elif method == 'solution':
        instance = Programming.objects.filter(video = value)
    elif method == 'pick':
        instance = Programming.objects.filter(status = 'Todo').order_by('?').first()
        context['problem'] = [instance.id,instance.title.lower().replace(" ","-")]
        return HttpResponse(json.dumps(context))
    listing = []
    for i in instance:
        d = {
            "id":i.id,
            "difficulty":i.difficulty,
            "status":i.status,
            "title":i.title,
            "tag":[j.category_name for j in i.tags.all()],

        }
        listing.append(d)


    

        
    
    context['problem'] = listing
    return HttpResponse(json.dumps(context))


def template(request,id):
    context = {}
    lang = request.GET.get('lang')
    method = request.GET.get('method')

    ins = Templates.objects.filter(instance = Programming.objects.get(id = id),language = Language.objects.get(lang = lang))
    if method == 'restore':
        context['instance'] = Language.objects.get(lang = lang).template
    elif method == 'Submitted':
        in1 = Submission.objects.filter(username = request.user,question = Programming.objects.get(id = id),language = Language.objects.get(lang = lang) )
        if in1.exists():
            context['instance'] = in1[0].solution
        else:
            context['instance'] = ins[0].code
    elif ins.exists():
        context['instance'] = ins[0].code
    else:
        context['instance'] = Language.objects.get(lang = lang).template
    return HttpResponse(json.dumps(context))

def save(request,id):
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('description')
        if not Templates.objects.filter(instance = Programming.objects.get(id = id),language = Language.objects.get(lang = title)).exists():
            instance = Templates(instance = Programming.objects.get(id = id),language = Language.objects.get(lang = title),code = desc)
            instance.save()
        else:
            ins = Templates.objects.get(instance = Programming.objects.get(id = id),language = Language.objects.get(lang = title))
            ins.code = desc
            ins.save()
        return HttpResponse(json.dumps('Saved'))


def runcode(request,id):
    if request.method == 'POST':
        program = Programming.objects.get(id = id)
        program.status = 'Attempted'
        program.save()
        title = request.POST.get('title')
        desc = request.POST.get('description')
        test = request.POST.get('case')
        ins = Templates.objects.get(instance = Programming.objects.get(id = id),language = Language.objects.get(lang = title))
        
        result=""

        return HttpResponse(json.dumps(result))


def like(request):
    value = request.GET.get('value')
    instance = Programming.objects.get(id = value)
    if request.user in instance.like.all():
        instance.like.remove(request.user)
        flag = False
    else:
        instance.like.add(request.user)
        flag = True
    like_count = instance.like.count()
    return HttpResponse(json.dumps([flag,like_count]))

def list(request):
    context = {}
    method = request.GET.get('method')
    value  = request.GET.get('value')
    ids = request.GET.get('ids')
    if method == 'add':
        
        program = Programming.objects.get(id = value)
        instance = Todo.objects.get(id = ids)
        if program not in instance.question.all():
            instance.question.add(program)
            instance.save()
            flag = True
            
        else:
            instance.question.remove(program)
            flag = False
        context['information'] = [f'{instance.title}',flag]
        return HttpResponse(json.dumps(context))
    else:
        ins = Todo(username = request.user,title = ids)
        ins.save()
        context['information'] = model_to_dict(ins)
        return HttpResponse(json.dumps(context))
