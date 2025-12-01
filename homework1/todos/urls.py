from django.urls import path
from . import views

app_name = 'todos'

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_todo, name='create'),
    path('edit/<int:pk>/', views.edit_todo, name='edit'),
    path('delete/<int:pk>/', views.delete_todo, name='delete'),
    path('toggle/<int:pk>/', views.toggle_resolve, name='toggle'),
]





