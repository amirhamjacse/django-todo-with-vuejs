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


    def post(self, request):
        task_datas = TaskSerializer(data=request.data, )
        if task_datas.is_valid():
            task_datas.save()
            return Response(task_datas.data, status=status.HTTP_201_CREATED)
        return Response(task_datas.data, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, *args, **kwarg):
        pk = self.kwargs['pk']
        task_intance = Task.objects.filter(pk=pk).last()