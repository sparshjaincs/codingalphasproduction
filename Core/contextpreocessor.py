from datetime import date
def utilities(request):
    context = {}
    
    context['days'] = date.today().strftime("%d")
    return context

