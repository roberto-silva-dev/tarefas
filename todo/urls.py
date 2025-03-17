from django.urls import path
from .views import task_list, task_create, task_handle

urlpatterns = [
    path('', task_list, name='task_list'),
    path('tasks/', task_create, name='task_create'),
    path('tasks/<int:task_id>/', task_handle, name='task_handle'),
]
