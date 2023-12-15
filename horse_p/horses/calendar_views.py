from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from horses.models import Calendar
from django.views.generic.list import ListView


 
def index(request):
    dates = Calendar.objects.all()
    
    return render(request,
                  "calendar.html",
                  context={'dates': dates,
                           })

