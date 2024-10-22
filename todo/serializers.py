from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        # fields = [
        #     'pk',
        #     'title',
        #     'description',
        #     'completed',
        #     'created_at',
        #     'due_date',
        # ]
        fields = '__all__'
