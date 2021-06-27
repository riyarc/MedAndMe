from django.urls import path
from . import views

urlpatterns = [
    path('add-measurement/', views.new_measurement, name="add-measurement"),
    path('add-group/', views.create_measurement_group, name="add-group"),
    path('view/', views.view_measurements, name="view_measurements"),
    path('delete/group/<int:pk>/', views.delete_group, name="delete_group"),
    path('delete/<int:pk>/', views.delete_measurement, name="delete_measurement"),

]
