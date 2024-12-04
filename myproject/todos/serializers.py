from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Tag

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 
            'user',
            'timestamp', 
            'title', 
            'description', 
            'due_date', 
            'tags', 
            'status'
        ]
        read_only_fields = ['timestamp', 'user']
