from django.contrib import admin
from django.urls import path
from App import views

urlpatterns = [
    path('', views.index, name='home'),
    path('find', views.find, name='find'),
    path('vacation', views.vacation, name='vacation'),
    path('about', views.aboutUs, name='about'),
    path('profile', views.profile, name='profile')
]
