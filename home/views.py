from django.shortcuts import render
from fundraising.models import *


# Create your views here.

def  home(request):
    last_4_copaign = Project_compaign.objects.all().order_by('-creation_date')[:4]
    return render(request,'home/home.html',{'last_4_copaign':last_4_copaign})

# def  base(request):
#     return render(request,'home/base.html')