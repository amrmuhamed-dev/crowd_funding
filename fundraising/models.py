from django.db import models
import datetime
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Project_compaign(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    details = models.TextField(max_length=2500)
    total_target = models.PositiveIntegerField()
    start_time = models.DateTimeField(blank=True)
    end_time = models.DateTimeField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str (self.title)


class Image(models.Model):
    image = models.ImageField(upload_to='project_img',max_length=800)
    compaign_img = models.ForeignKey(Project_compaign,related_name='images', on_delete=models.CASCADE)


    # pictures = ArrayField(ArrayField
    #                       (models.ImageField(upload_to='project_img', max_length=800),size=4),size=4,)

    def __str__(self):
        return str (self.image)

   
class Category(models.Model):
    # category_choices = (("theater","Theater"),("crafts","Crafts"),
    #                     ("design","Design"),("fashion","Fashion"),
    #                     ("food","Food"), ("games","Games"),
    #                     ("journalism","Journalism"),("photography","Photography"),
    #                     ("technology","Technology"),)

    category = models.CharField(max_length=50)
    compaign_categ = models.ForeignKey(Project_compaign,related_name='category', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.category)

class Donations(models.Model):
    compaign = models.ForeignKey(Project_compaign,on_delete=models.CASCADE)
    donnator = models.ForeignKey(User,on_delete=models.CASCADE)
    donation = models.FloatField()
    donation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.donation)

class Comments(models.Model):
    comment = models.TextField()
    compaign = models.ForeignKey(Project_compaign, on_delete=models.CASCADE)
    commentor = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Reply(models.Model):
    reply = models.CharField()
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    replier = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment_report(models.Model):
    report =  models.CharField(max_length=200,blank=True)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Compaign_report(models.Model):
    report =  models.CharField(max_length=200,blank=True)
    compaign = models.ForeignKey(Project_compaign, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Rating(models.Model):
    project = models.ForeignKey(Project_compaign,on_delete=models.CASCADE)
    rater = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    rating_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating)
    







