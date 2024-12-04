from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling CRUD operations on Tasks.
    
    Provides the following endpoints:
    - GET /tasks/: List all tasks
    - GET /tasks/{id}/: Retrieve a specific task
    - POST /tasks/: Create a new task
    - PUT /tasks/{id}/: Update an entire task
    - PATCH /tasks/{id}/: Partially update a task
    - DELETE /tasks/{id}/: Delete a task
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    # Add authentication and permission classes
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Ensure users can only see their own tasks
        """
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically set the user when creating a task
        """
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Custom create method to handle task creation.
        Ensures that timestamp is not manually set.
        """
        # Remove timestamp if manually provided
        if 'timestamp' in request.data:
            del request.data['timestamp']
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        """
        Custom update method to prevent timestamp modification.
        """
        # Remove timestamp from update request
        if 'timestamp' in request.data:
            del request.data['timestamp']
        
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Custom partial update method to prevent timestamp modification.
        """
        # Remove timestamp from partial update request
        if 'timestamp' in request.data:
            del request.data['timestamp']
        
        return super().partial_update(request, *args, **kwargs)
