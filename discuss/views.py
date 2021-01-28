from django.shortcuts import render

# Create your views here.
def homepage(request):
    context = {}
    method = request.GET.get('method')
    if method is None or method == "" or method == 'General':
        context['method'] = 'General'
    else:
        context['method'] = method
    return render(request,'discuss/homepage.html',context)