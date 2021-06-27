from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('view/', views.view_blog, name= 'view_blog')
]
