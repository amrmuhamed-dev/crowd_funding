from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Userprofile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=11)
    phone_number = models.CharField(max_length=15, null=True)
    picture = models.ImageField(upload_to='profile_img/',max_length=81200)
    birthdate = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True)
    fb_account = models.URLField(max_length=50,blank=True)
    forget_password_token = models.CharField(max_length=100,null=True)
    email_activate_token = models.CharField(max_length=100,null=True)
    is_activated = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    