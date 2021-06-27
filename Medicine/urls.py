from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.view_medicines, name="view_medicines"),
    path('add/', views.medicine_form, name="add_medicine"),
    path('', views.medicine, name="medicine"),
    path('delete/<int:pk>/', views.delete_medicine, name="delete_medicine"),
    path('view/current/', views.view_current_medicines, name="current_medicines"),
]
