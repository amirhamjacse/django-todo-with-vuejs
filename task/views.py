from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from .models import Task
from .serializers import TaskSerializer


class TaskView(APIView):
    def get(self, request):
        task_objects = Task.objects.all()
        serialize = TaskSerializer(task_objects, many=True )
        return Response(data = serialize.data, status=status.HTTP_200_OK)
    