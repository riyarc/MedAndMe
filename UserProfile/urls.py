from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_page, name='login'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('logout/', views.logout_page, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('graph/', views.graph, name='graph'),
    path('search/', views.search, name='search'),
    path('search_page/', views.search_page, name='search_page'),
]
