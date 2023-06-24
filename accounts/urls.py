from django.contrib import admin
from django.urls import path,include
from accounts.views import *
from django_email_verification import urls as mail_urls
from django.conf import settings

urlpatterns = [
    # path('userprofile/',userprofile,name="userprofile"),
    path('register',Useregister,name='register'),
    path('login',Userlogin,name='login'),
    path('logout',Userlogout,name='logout'),
    path('forget-password/' , ForgetPassword , name="forget_password"),
    path('change-password/<token>/' , ChangePassword , name="change_password"),
    path('delete',Deleteaccounts, name='deleteaccounts'),
    path('update_password',Update_password,name='update_password'),
    path('profile/<int:user_id>/',userprofile,name='profile'),
    path('profileupdate',Profileupdate,name='profileupdate'),
    path('email/',include(mail_urls),name='mail_urls'),
    path('sendemail/' , Sendemail , name="sendemail"),
    path('emailactivate/<token>/' , Emailactivate , name="emailactivate"),
    path('profile/compaign_details/<int:compaign_id>/',User_compaign_details,name='compaign_details')
]+static(settings.MEDIA_DIR, document_root=settings.MEDIA_ROOT)
