from django import template
import json as js
register = template.Library()

@register.filter
def replace(value):
    value = value.lower()
    return value.replace(" ","-")

@register.filter
def split(value,field):
    return value.split(field)

@register.filter
def remove(value):
    return value.split(",")

@register.filter
def strip(value):
    return value.strip(" ")

@register.filter
def remove(value):
    return value.split(",")


@register.filter
def addhyphen(value):
    return "_".join(value.split(" "))

@register.filter
def getlatest(value):
    value = list(value)
    value.sort(key=lambda x:(x.date,x.time),reverse = True)
    if len(value) == 0:
        value = ["Write Your First Anwser.."]
    else:
        value = value
    return value

@register.filter
def latest(value):
    value = list(value)
    value.sort(key=lambda x:(x.date,x.time),reverse = True)
    if len(value) == 0:
        value = ["Write Your First Anwser.."]
    else:
        value = [value[0]]
    return value

@register.filter
def json(value):
    value = value.split(",")
    return value


@register.filter
def sorting(value):
    value = value.order_by('-score')
    return value

@register.filter
def multiply(value,arg):
    return value*arg

@register.filter
def check(value,arg):
    val = 2
    try:
        if arg[value.question_id] == value.correct:
            val = 1
        elif arg[value.question_id] != value.correct:
            val = 0
    except:
        val=2
   

    return val

@register.filter
def check1(value,arg):

    return arg[value.question_id]

@register.filter
def in_category(things, category):
    return things.filter(category=category)

@register.filter
def compare_length(value,arg):
    if len(value) > arg:
        return True
    else:
        return False