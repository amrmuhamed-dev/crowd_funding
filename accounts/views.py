from django.http import HttpResponse
from django.shortcuts import  render, get_object_or_404, redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from fundraising.models import *
from django.contrib import messages
from django.conf.urls.static import static
from typing import Protocol
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
# from django_email_verification import sendconfirm
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.conf import settings
from django.contrib.auth import authenticate,login,logout
from.helpers import send_forget_password_mail
from.helpers import send_email_activate
# Create your views here.
# done------------------------------------------------------------------------->
def Useregister(request):

    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email = request.POST['email']
    email = request.POST['email']
    phone = request.POST['phone']
    # --------------------------very important----------------------#
    profile_img = request.FILES['image']

    # --------------------------very important----------------------#
    user_name =request.POST['user_name']
    birth_date= request.POST['birth_date']
    country = request.POST['country']
    fb_account = request.POST['fb_account']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

        if User.objects.filter(email=email).count() > 0:
            messages.error(request, "This email is already exists" )
            return render(request,'accounts/register.html')
        
        if User.objects.filter(username=user_name).count() > 0:
            messages.error(request, "This user name is already exists" )
            return render(request,'accounts/register.html')
        
        emailnumeric=email.isnumeric()
        if emailnumeric:
            messages.error(request, "email can not be numbers" )
            return render(request,'accounts/register.html')
        
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters" )
            return render(request, 'accounts/register.html')
        

        if password == confirm_password:
    user = User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=user_name ,password=password,is_active=False)
    user.save()
    user_profile = Userprofile.objects.create(user=user,birthdate=birth_date,picture=profile_img,mobile=phone,country=country,fb_account=fb_account)
    user_profile.save()
    token = str(uuid.uuid4())
    user_profile.email_activate_token = token
    user_profile.save()
    send_email_activate(user.email , token)
    messages.success(request, 'A verification email is sent.')
    return redirect('login')
        else:
            return redirect('register')

    return render(request, 'accounts/register.html')
# done------------------------------------------------------------------------->
def  Userlogin(request):
        # username = request.POST.get('username')
        # password =request.POST.get('password')
        if request.method=='POST':
          username = request.POST.get('username')
          password =request.POST.get('password')

          if User.objects.filter(username=username).count()<1:
              messages.error(request, "Invalid username or password" )
              return render(request,'accounts/login.html')
          
          if not User.objects.get(username=username).is_active:
              messages.error(request, 'Your account is not active')
              return redirect('login')
          user = authenticate(request,username=username,password=password)
          if user: 
              login(request,user)
              request.session['username']=request.POST['username']
              return redirect('home')  
          else:
                messages.error(request, "This Username is not exists or Pssword Incorrect" )
                return render(request,'accounts/login.html')
        return render(request,'accounts/login.html')
# done------------------------------------------------------------------------->
@login_required
def Userlogout(request):
    logout(request)
    return redirect('home')
# done------------------------------------------------------------------------->

@login_required
def userprofile(request,user_id):
    current_user=Userprofile.objects.get(user_id=user_id)
    user_compaign = Project_compaign.objects.filter(creator=current_user.user)
    categories=Category.objects.all()
    donations = Donations.objects.all()
    return render(request,'accounts/profile.html',{'current_user':current_user,'user_compaign':user_compaign,'categories':categories,'donations':donations})

@login_required
def User_compaign_details(request,compaign_id):
    compaign = Project_compaign.objects.get(pk=compaign_id)
    category=Category.objects.get(compaign_categ=compaign_id)
    image = Image.objects.filter(compaign_img=compaign_id)
    counter=[]
    for i in image:
        counter.append("1")
    counter.pop()


    comments = Comments.objects.filter(compaign=compaign_id)
    replies = Reply.objects.all()
    context={'compaign':compaign,'category':category,'image':image,'comments':comments,'replies':replies,'counter':counter}
    return render(request,'accounts/compaign_details.html',context)
# done------------------------------------------------------------------------->
@login_required
def Profileupdate(request):
    user=request.user
    current_user=Userprofile.objects.get(user_id=user)
    if request.method=='POST':
        if current_user.user.email!=request.POST['email']:
            messages.error(request, "Can not change email ")
            return render(request, 'accounts/login.html')
        else:
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            username=request.POST['user_name']
            picture=request.FILES['image']
            birthdate=request.POST['birth_date']
            mobile=request.POST['phone']
            country=request.POST['country']
            fb_account=request.POST['fb_account']
            User.objects.filter(pk=user.id).update(first_name=first_name,last_name=last_name,username=username)
            Userprofile.objects.filter(user=user.id).update(birthdate=birthdate,picture=picture,mobile=mobile,country=country,fb_account=fb_account)
            return redirect('profile',user.id)
    return render(request, 'accounts/profileupdate.html',{'current_user':current_user})

def Update_password(request):
    user=request.user
    current_user=Userprofile.objects.get(user_id=user.id)
    if request.method=='POST':
            if current_user.user.check_password(request.POST['old_password'])==False:
                messages.error(request, "The old password incorrect " )
                return render(request, 'accounts/update_password.html',{'current_user':current_user})
                
            
            if current_user.user.check_password(request.POST['new_password'])==True:
                messages.error(request, "The old password cannot be the same as the new password " )
                return render(request, 'accounts/update_password.html',{'current_user':current_user})

            if len(request.POST['new_password']) < 8:
                messages.error(request, "Password must be at least 8 characters" )
             
                return render(request, 'accounts/update_password.html',{'current_user':current_user})
            
            else:
                current_user.user.set_password(request.POST['new_password'])
                current_user.user.save()
                logout(request)
                return redirect('login')
    return render(request,'accounts/update_password.html',{'current_user':current_user})
import uuid
# UUID(Universal Unique Identifier) is a Python library that generates random objects of 128 bits.
def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            
            if not User.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('forget-password')
            
            user_obj = User.objects.get(username = username)
            token = str(uuid.uuid4())
            profile_obj= Userprofile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'An email is sent.')
            return redirect('/forget-password/')
                
    
    
    except Exception as e:
        print(e)
    return render(request , 'accounts/forget-password.html')
def ChangePassword(request , token):
    context = {}
    
    
    try:
        profile_obj = Userprofile.objects.filter(forget_password_token = token).first()
        context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')
                
            
            if  new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')
            if len(new_password) < 8:
                messages.error(request, "Password must be at least 8 characters" )
                return redirect(f'/change-password/{token}/')
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request, 'Password Updated Successfully')
            return redirect('login')
              
        
    except Exception as e:
        print(e)
    return render(request , 'accounts/change-password.html' , context)
def Sendemail(request,user_profile):
    token = str(uuid.uuid4())
    send_email_activate(user_profile.user.email , token)
    messages.success(request, 'A verification email is sent.')
    return redirect('login')
def Emailactivate(request, token):
    try:
        profile_obj = Userprofile.objects.get(email_activate_token = token)
        # profile_obj.is_activated = "True"
        if profile_obj.user.is_active==True :
            messages.error(request, 'Your Email Is Already Activated.')
            return redirect('login')
        else:       
            profile_obj.user.is_active = "True"
            profile_obj.save()
            profile_obj.user.save()
            messages.success(request, 'Your Email Is Activated Now...')
            return redirect('login')             
          
    except Exception as e:
        print(e)
    return redirect(request ,'login')
@login_required
def Deleteaccounts(request):
    request.user.delete()
    return redirect('logout')