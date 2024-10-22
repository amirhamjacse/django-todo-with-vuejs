from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer


class TaskView(APIView):
    def get(self, request):
        task = Task.objects.all().order_by('pk')
        serialize_data = TaskSerializer(task, many=True)
        # print(serialize_data, 'seria---------')
        return Response(serialize_data.data, status=status.HTTP_200_OK)


    def post(self, request):
        serialize_data = TaskSerializer(data=request.data)
        # print(serialize_data, '------------------serialize data')
        if serialize_data.is_valid():
            serialize_data.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        # print(pk, 'pkk---------------')
        # print(pk, 'workingssss')
        instance = Task.objects.filter(pk=pk).last()
        # print(instance.id, 'instances')
        serilize_data = TaskSerializer(instance, request.data)
        if serilize_data.is_valid():
            serilize_data.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        instance = Task.objects.filter(pk=pk).last()
        # print(instance, 'insss')
        serialize_data = TaskSerializer(instance, request.data, partial=True)
        if serialize_data.is_valid():
            serialize_data.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        try:
            instance = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
