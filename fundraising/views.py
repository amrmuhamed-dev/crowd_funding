import datetime
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from .models import *
from django.contrib import messages
from django.http import HttpResponse,Http404
from django.contrib.auth.models import User
from django.shortcuts import  render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.db.models import Count
from datetime import datetime


@login_required
def create_campaign(request):
    username=request.session['username']
    user = User.objects.get(username=username)
    if request.user.is_authenticated:
        if request.method=='POST':
            title = request.POST['title']
            details = request.POST['details']
            total_target = request.POST['target']
            start_time = request.POST['start_time']
            end_time = request.POST['end_time']
            category= request.POST['category']
            images = request.FILES.getlist('image')

            project_compaign = Project_compaign.objects.create(creator=user, title=title,details=details,total_target=total_target,start_time=start_time,end_time=end_time)
            project_compaign.save()

            for img in images:
                image=Image.objects.create(image=img,compaign_img=project_compaign)
                image.save()
            category = Category.objects.create(category=category,compaign_categ=project_compaign)
            category.save()

            return redirect('profile',user.id)
    else:
        return redirect('login')
    return render(request, 'fundraising/create_campaign.html')

@login_required
def Update_campaign(request,compaign_id):
    user=request.user
    compaign = get_object_or_404(Project_compaign,pk=compaign_id)
    if request.method=='POST':
        title = request.POST['title']
        details = request.POST['details']
        total_target = request.POST['target']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        new_category= request.POST['category']
        images = request.FILES.getlist('image')
        Project_compaign.objects.filter(pk=compaign_id).update(title=title,details=details,total_target=total_target,
                                                       start_time=start_time,end_time=end_time)
        Category.objects.filter(compaign_categ=compaign_id).update(category=new_category)
        for img in images:
           Image.objects.filter(pk=compaign_id).update(image=img)
        return redirect('profile',user.id)
    myDate = datetime.now()
    return render(request, 'fundraising/update_compaign.html',{'compaign':compaign,'myDate':myDate})

@login_required
def Delete_campaign(request,compaign_id):
     compaign = get_object_or_404(Project_compaign,pk=compaign_id)
     image = get_object_or_404(Image,pk=compaign.pk)
     category = get_object_or_404(Category,pk=compaign.pk)
     compaign.delete()
     image.delete()
     category.delete()
     return redirect('home')

def All_compaign(request):
    all_compaign =Project_compaign.objects.all()
    return render(request,'fundraising/all_compaign.html',{'all_compaign':all_compaign})

@login_required
def Add_comment(request,compaign_id):
    user = request.session
    if not user:
        return redirect('login')
    if request.method == "POST":
        if request.POST['comment']:
            user = request.user
            comment = request.POST['comment']
            compaign = Project_compaign.objects.get(pk=compaign_id)
            Comments.objects.create(comment=comment,compaign=compaign,commentor=user)
        return redirect('compaign_details',compaign_id)
    return render(request, "accounts/compaign_details.html")    

@login_required
def Reply_comment(request):    
    user = request.session
    if not user:
        return redirect('login')
    if request.method == "POST":
        if request.POST['reply']:
            user = request.user
            reply = request.POST['reply']
            commentpk=request.POST['commentpk']
            compaignpk=request.POST['compaignpk']
            comment_id = Comments.objects.get(pk=commentpk)
            reply = Reply.objects.create(reply=reply,comment=comment_id,replier=user)
        return redirect('compaign_details',compaignpk)
    return render(request, "accounts/compaign_details.html")    

def Report_compaign(request, compaign_id):
    user = request.session
    if not user:
        return redirect('login')

    else:
        user = request.user
        compaign = Project_compaign.objects.get(pk=compaign_id)
        if request.method == "POST":
            report = request.POST['report']
            Compaign_report.objects.create(report=report,compaign=compaign,user=user)
            return redirect('compaign_details', compaign.id)
    return render(request, "accounts/compaign_details.html")


def Report_comment(request, comment_id):
    user = request.session
    if not user:
        return redirect('login')
    else:
        user = request.user
        comment = Comments.objects.get(pk=comment_id)
        compaign = comment.compaign
        if request.method == "POST":
            report = request.POST['report']
            Comment_report.objects.create(report=report,comment=comment,user=user)
            return redirect('compaign_details',compaign.id)
        
    return render(request, "accounts/compaign_details.html")

@login_required
def Donate_compaign(request, compaign_id):
    user = request.user
    if not user:
        return redirect('login')
    else:
        user = request.user
        if request.method == "POST":
            if request.POST['donate']:
                compaign = Project_compaign.objects.get(pk=compaign_id)
                donate = request.POST['donate']
                Donations.objects.create(compaign=compaign,donnator=user,donation=donate)
                return redirect('compaign_details', compaign_id)
            
    return render(request, "accounts/compaign_details.html")

@login_required
def Search(request):
    user = request.user
    if not user:
        return redirect('login')
    
    else:
        user = request.user
        "strip():Remove spaces at the beginning and at the end of the string:"
        if request.method == "POST":
            search=request.POST['search']
            if len(search.strip()) > 0:
                searched_compaign = Project_compaign.objects.filter(title__icontains=search)
                return render(request,'fundraising/searched_compaign.html',{'searched_compaign':searched_compaign})    

                       
            elif len(search.strip()) <= 0:
                    messages.success(request,'No Projects Found') 


            return render(request, "fundraising/searched_compaign.html")
        
        
    return render(request, "home/home.html")

