from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.allergy_main, name='allergy_main'),
    path('add/', views.add_allergy, name='add_allergy'),
    path('view/', views.view_allergy, name='view_allergy'),
    path('delete/<int:pk>/', views.delete_allergy, name='delete_allergy'),
]
