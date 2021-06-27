from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_record, name="add_record"),
    path('view/', views.view_records, name="view_records"),
    path('view/<int:pk>/', views.view_record, name="view_record"),
    path('delete/file/<int:pk>/', views.delete_file, name="delete_file"),
    path('delete/<int:pk>/', views.delete_record, name="delete_record"),
    path('add/<int:pk>/', views.add_files, name="add_files"),
    path('view/pdf/<path:file_path>', views.view_pdf, name="view_pdf"),
]
