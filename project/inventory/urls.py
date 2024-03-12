from django.urls import path
from . import views

urlpatterns = [
path('companies/', views.company_list, name='company_list'),
path('roles/', views.role_list, name='role_list'),

]