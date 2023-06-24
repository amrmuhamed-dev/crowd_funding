from django.contrib import admin
from django.urls import path
from home.views import *


urlpatterns = [
path('home',home,name='home'),
# path('base',base,name='base'),
]