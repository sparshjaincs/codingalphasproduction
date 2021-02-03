from django.shortcuts import render
#from .models import *
from celery.schedules import crontab
from celery.task import periodic_task
from datetime import date
import calendar
@periodic_task(run_every=crontab(hour = 0,minute =0 ,day_of_month = 1))
def every_monday_morning():
    time = date.today()
    intyear = time.strftime("%m")
    month = time.strftime("%B")
    year = time.strftime("%Y")
    title = f"{month} CodingAlpahs Coding Challange {year}"
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
        try:
            ins2 = ContestContent(instance = ins,chapter_instance = ins1, title = title)
            ins2.save()
        except Exception as exp:
            pass
        
        c+=1

    
# Create your views here.
def homepage(request):
    return render(request,'Explore/homepage.html')
#every_monday_morning()


