
from drf_yasg import openapi
from task.views import TaskView
from django.urls import path, re_path, include
from rest_framework import permissions

urlpatterns = [
    path('taskget/', TaskView.as_view(), name='taskviews'),
    # path('task/update/<int:pk>/', TaskView.as_view(), name='taskupdate'),
    # path('task/delete/<int:pk>/', TaskView.as_view(), name='taskdelete'),
    # # path('task/partial/update/<int:pk>/', TaskView.as_view(), name='taskupdate_partial'),
]
