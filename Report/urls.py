from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_report, name="add_report"),
    path('view/', views.view_reports, name="view_reports"),
    path('view/<int:pk>/', views.view_report, name="view_report"),
    path('delete/file/<int:pk>/', views.delete_file, name="delete_file"),
    path('delete/<int:pk>/', views.delete_report, name="delete_report"),
    path('add/<int:pk>/', views.add_files, name="add_files"),
    path('view/pdf/<path:file_path>/', views.view_pdf, name="view_pdf")
]
