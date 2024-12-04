from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Task, Tag

class TaskViewSetIntegrationTest(TestCase):
    def setUp(self):
        """
        Set up test data and authentication
        """
        # Create test users
        self.user1 = User.objects.create_user(
            username='user1', 
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2', 
            password='testpass456'
        )
        
        # Create API client
        self.client = APIClient()
        
        # Authenticate user1
        self.client.force_authenticate(user=self.user1)
        
        # Create a test tag
        self.tag = Tag.objects.create(name='Test Tag')
        
        # Create initial tasks
        self.task1 = Task.objects.create(
            user=self.user1,
            title='User1 Task 1',
            description='First task for user1',
            status=Task.StatusChoices.OPEN
        )
        self.task2 = Task.objects.create(
            user=self.user1,
            title='User1 Task 2',
            description='Second task for user1',
            status=Task.StatusChoices.WORKING
        )
    
    def test_create_task(self):
        """
        Test creating a new task
        """
        task_data = {
            'title': 'New Task',
            'description': 'Task created via API',
            'status': Task.StatusChoices.OPEN
        }
        
        response = self.client.post(
            reverse('task-list'), 
            task_data, 
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(response.data['title'], 'New Task')
        self.assertEqual(response.data['user']['username'], 'user1')
    
    def test_list_tasks(self):
        """
        Test listing tasks for authenticated user
        """
        response = self.client.get(reverse('task-list'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Only user1's tasks
    
    def test_retrieve_task(self):
        """
        Test retrieving a specific task
        """
        response = self.client.get(
            reverse('task-detail', kwargs={'pk': self.task1.id})
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'User1 Task 1')
    
    def test_update_task(self):
        """
        Test updating an existing task
        """
        update_data = {
            'title': 'Updated Task Title',
            'description': 'Updated description',
            'status': Task.StatusChoices.COMPLETED
        }
        
        response = self.client.put(
            reverse('task-detail', kwargs={'pk': self.task1.id}),
            update_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh task from database
        updated_task = Task.objects.get(id=self.task1.id)
        self.assertEqual(updated_task.title, 'Updated Task Title')
        self.assertEqual(updated_task.status, Task.StatusChoices.COMPLETED)
    
    def test_partial_update_task(self):
        """
        Test partially updating a task
        """
        partial_update_data = {
            'status': Task.StatusChoices.PENDING_REVIEW
        }
        
        response = self.client.patch(
            reverse('task-detail', kwargs={'pk': self.task1.id}),
            partial_update_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh task from database
        updated_task = Task.objects.get(id=self.task1.id)
        self.assertEqual(updated_task.status, Task.StatusChoices.PENDING_REVIEW)
    
    def test_delete_task(self):
        """
        Test deleting a task
        """
        response = self.client.delete(
            reverse('task-detail', kwargs={'pk': self.task1.id})
        )
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)
    
    def test_cross_user_task_access(self):
        """
        Test that users cannot access tasks of other users
        """
        # Authenticate user2
        self.client.force_authenticate(user=self.user2)
        
        # Try to access user1's task
        response = self.client.get(
            reverse('task-detail', kwargs={'pk': self.task1.id})
        )
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
