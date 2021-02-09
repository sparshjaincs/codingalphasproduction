from django.shortcuts import render
from .models import *
from celery.schedules import crontab
from celery.task import periodic_task
from datetime import date
import calendar
import random
@periodic_task(run_every=crontab(hour = 0,minute =0 ,day_of_month = 1))
def every_monday_morning():
    time = date.today()
    intyear = time.strftime("%m")
    month = time.strftime("%B")
    year = time.strftime("%Y")
    title = f"CodingAlphas {month} Coding Challenge {year}"
    try:
        ins = DailyContest(title = title)
        ins.save()
    except:
        ins = DailyContest.objects.get(title = title)
    days = calendar.monthrange(int(year),int(intyear))
    c=1
    for i in range(1,days[1]+1,7):

        if i+6>days[1]+1:
            last = days[1]
        else:
            last = i+6
       
        title = f"Week {c} : {month} {i}th - {last}th"
        try:
            ins1 = ContestChapter(instance = ins,title = title)
            ins1.save()
        except Exception as exp:
            ins1 = ContestChapter.objects.get(instance = ins,title = title)
        
        collect = Programming.objects.all().order_by('?')[:7]
        
        c1 = 0
        while ContestContent.objects.filter(instance = ins,chapter_instance = ins1).count() <= (last-i):
            
            
            ins2 = ContestContent(instance = ins, chapter_instance = ins1,question = collect[c1])
            ins2.save()
            c1+=1

        c+=1

    
# Create your views here.
def homepage(request):
    context = {}
    context['date'] = date.today().strftime("%d")
    context['chapter'] = DailyContest.objects.all().order_by('created')
    return render(request,'Explore/homepage.html',context)
every_monday_morning()

def daily(request,title,id):
    context = {}
    data = DailyContest.objects.get(id = id)
    context['data'] = data
    n = int(date.today().strftime("%d"))

    if n%7 == 0:
        flag = n//7-1
    else:
        flag = n//7
    
    context['date'] = date.today()
    c = 0
    content= []
    con = 0
    for i in data.contestchapters.all():
        l = {}
        l['title'] = i.title
        l['id'] = i.id
        if flag > c:
            status = 'Expired'
        elif flag == c:
            status = 'Active'
        else:
            status = 'Upcoming'
        l['status'] = status
        ques= []
        
        for j in i.chaptercontent.all():
            df= {}
            df['id'] = j.question.id
            if con < n:
                df['instance'] = j
                if con == n-1:
                    df['flag'] = True
            ques.append(df)
            con+=1
        l['question'] = ques
        content.append(l)
        c+=1
    context['content'] = content


    return render(request,'Explore/chapter.html',context)

def dailytest(request,id,title,quesid):
    context = {}
    context['title'] = ContestChapter.objects.get(id = id)
    context['problem'] = Programming.objects.get(id = quesid)
    context['language'] = Language.objects.all()
    return render(request,'Explore/dailytest.html',context)

