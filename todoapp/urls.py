from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('register/', views.register, name='registration-page'),
    path('login/', views.loginpage, name='login-page'),
    path('todos/', views.todopage, name='todo-page'),
    path('logout/', views.logout_view, name='logout'),
    path('task/update/<int:task_id>/', views.update_task_status, name='update-task-status'),
    path('task/delete/<int:task_id>/', views.delete_task, name='delete-task'),
]
