from django.shortcuts import render
from .models import *
from django.http import HttpResponse
import json
from .compile import Compiler
from .tokens import *
from django.views.decorators.clickjacking import xframe_options_exempt
# Create your views here.
def playground(request,file_name="Untitled"):
    context = {}
    context['play'] = PlayGround.objects.filter(user = request.user)
    
    return render(request,'playground/playground.html',context)

def emptyplay(request,var):
    context = {} 
    context['language'] = Language.objects.all()
    if var == 'empty':
        file_name = 'Untitled'
        ins = PlayGround(user = request.user,title=file_name)
        ins.save()
        context['id'] = ins.id
        instance = Language.objects.all().first()
        context['instance'] = instance.template
        context['file_name'] = 'Untitled'
        return render(request,'playground/rendering.html',context)
    else:
        var = int(var)
        if request.user == PlayGround.objects.get(id = var).user:
            if ExtendPlay.objects.filter(instance = PlayGround.objects.get(id = var),lang = Language.objects.all().first()).exists():
                ins  =ExtendPlay.objects.get(instance = PlayGround.objects.get(id = var),lang = Language.objects.all().first())
                context['instance'] = ins.code
            else:
                instance = Language.objects.all().first()
                context['instance'] = instance.template
            context['id'] = var
            context['file_name'] = PlayGround.objects.get(id = var).title
            return render(request,'playground/rendering.html',context)
        else:
            return render(request,'Core/snippets/404.html')

def savefile(request,id):
    ins = PlayGround.objects.get(id = id)
    ins.title = request.GET.get('file_name')
    ins.save()
    return HttpResponse(json.dumps('Saved'))

def save(request,id):
    if request.method == 'POST':
        data = request.POST.get('description')
        lang = request.POST.get('title')
        if ExtendPlay.objects.filter(instance = PlayGround.objects.get(id = id),lang = Language.objects.get(lang = lang)).exists():
            ins = ExtendPlay.objects.get(instance = PlayGround.objects.get(id = id),lang = Language.objects.get(lang = lang))
            ins.code = data
            ins.save()
        else:
            instance = ExtendPlay(instance = PlayGround.objects.get(id = id),lang = Language.objects.get(lang = lang),code = data)
            instance.save()
    return HttpResponse(json.dumps('Auto Saved'))


def temp(request,id):
    context = {}
    lang = request.GET.get('lang')
    if ExtendPlay.objects.filter(instance = PlayGround.objects.get(id = id),lang = Language.objects.get(lang = lang)).exists():
        ins = ExtendPlay.objects.get(instance = PlayGround.objects.get(id = id),lang = Language.objects.get(lang = lang))
        context['instance'] = ins.code
    else:

        instance = Language.objects.get(lang = lang)
        context['instance'] = instance.template
    context['lang'] = lang
    return HttpResponse(json.dumps(context))

def test(request):
    if request.method == 'POST':
        context = {}
        data = request.POST.get('description')
        lang = request.POST.get('title')
        input_val = request.POST.get('input')
        if input_val is None:
            context['output'] = [['Invalid Input'],'N/A']
            return HttpResponse(json.dumps(context))
        input_val = input_val.split("\n")
        cp = Compiler()
        result = cp.execute(data,lang,input_val)
        context['output'] = result

        return HttpResponse(json.dumps(context))


def frontend(request,var):
    context = {}
    context['snippet'] = Libraries.objects.all()
    if var == 'empty':
        file_name = 'Untitled'
        ins = PlayGround(user = request.user,title=file_name,category='Frontend')
        ins.save()
        ty_ob = {
            'id':ins.id,
            'method':'Frontend',
            'share':True,
        }
        ty_embed = {
            'id':ins.id,
            'method':'Frontend',
            'share':True,
            'embed':True,
        }
        ins = PlayGround.objects.get(id=ins.id)
        link = request.get_host()+'/playground/share/'+get_secret_key(ty_ob)+'/'
        ins.link = link
        ins.embed =  request.get_host()+'/playground/embed/'+get_secret_key(ty_embed)+'/'
        ins.save()
        context['id'] = ins.id
        context['file_name'] = 'Untitled'
        context['link'] = ins.link
        context['live_status'] = False

        return render(request,'playground/frontend.html',context)
    else:
        var = int(var)
        if request.user == PlayGround.objects.get(id = var).user:
            context['id'] = var
            context['file_name'] = PlayGround.objects.get(id = var).title
            context['link'] = PlayGround.objects.get(id = var).link
            context['live_status'] = PlayGround.objects.get(id = var).live
            return render(request,'playground/frontend.html',context)
        else:
            return render(request,'Core/snippets/404.html')
  

def load(request):
    return render(request,'playground/front_temp/front.html')

def frontend_run(request):
    if request.method == 'POST':
        method = request.POST.get('method')
        html = request.POST.get('html')
        css = request.POST.get('css')
        js = request.POST.get('js')
        ids = request.POST.get('id')
        if method == 'write':
            data = html.split('<meta charset="utf-8">')
            s = data[0] + f'''<meta charset="utf-8">
            <style>{css}
            </style>
            '''+data[-1]
            data = s.split("</body>")
            s = data[0] + f'''
            <script>
            {js}
            </script>
            ''' + data[-1]
            fp = open('./Playground/templates/playground/front_temp/front.html','w')
            fp.write(s)
            fp.close()
        

            return HttpResponse(json.dumps('Done'))
        elif method == 'Save':
            if ExtendFrontend.objects.filter(instance = PlayGround.objects.get(id = ids)).exists():
                ins = ExtendFrontend.objects.get(instance = PlayGround.objects.get(id = ids))
                ins.html = html
                ins.css = css
                ins.js = js
                ins.save()
            else:
                ins = ExtendFrontend(instance = PlayGround.objects.get(id = ids),html=html,css=css,js=js)
                ins.save()
            return HttpResponse(json.dumps('Saved'))


def template_load(request):
    template = request.GET.get('template')
    ids = request.GET.get('id')
    if template == 'Saved' and ExtendFrontend.objects.filter(instance = PlayGround.objects.get(id = ids)).exists():
        frontend = ExtendFrontend.objects.get(instance = PlayGround.objects.get(id = ids))
    else:
        if template == 'Saved':
            template = 'Default'
        frontend = Frontend.objects.get(method = Libraries.objects.get(template = template))
    context = {}
    context['html'] = frontend.html
    if frontend.scss:
        context['css'] = frontend.scss
        context['scss'] = True
    else:
        context['css'] = frontend.css
        context['scss'] = False
    context['js'] = frontend.js
    return HttpResponse(json.dumps(context))

def share(request,token):
    context={}
    data = verify_secret_key(token)
    context['snippet'] = Libraries.objects.all()
    if data['method'] == 'Frontend':
        ins = PlayGround.objects.get(id = data['id'])
        context['id'] = data['id']
        context['file_name'] = ins.title
        if ins.live:
            context['share'] = False
            context['Live'] = True
        else:
            context['share'] = data['share']
            context['Live'] = False
        context['user'] = ins.user
        context['link'] = ins.link
        return render(request,'playground/frontend.html',context)

def live(request):
    var = request.GET.get('var')
    ins = PlayGround.objects.get(id= var)
    if ins.live:
        ins.live = False
        status = 0
    else:
        ins.live = True
        status = 1
    ins.save()
    return HttpResponse(json.dumps(status))
@xframe_options_exempt
def embed(request,token):
    context={}
    data = verify_secret_key(token)
    context['snippet'] = Libraries.objects.all()
    if data['method'] == 'Frontend':
        ins = PlayGround.objects.get(id = data['id'])
        context['id'] = data['id']
        context['file_name'] = ins.title
        context['embed'] = data['embed']
        context['user'] = ins.user
        context['link'] = ins.link

    return render(request,'playground/embed.html',context)



