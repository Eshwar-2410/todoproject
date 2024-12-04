from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from ..models import Task, Tag
from datetime import timedelta

class TaskModelTest(TestCase):
    def setUp(self):
        """
        Set up test data for Task model tests
        """
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass123'
        )
        
        # Create a test tag
        self.tag = Tag.objects.create(name='Test Tag')
    
    def test_task_creation(self):
        """
        Test creating a task with all required fields
        """
        task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test Description',
            status=Task.StatusChoices.OPEN
        )
        
        # Check task creation
        self.assertTrue(isinstance(task, Task))
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.description, 'Test Description')
        self.assertEqual(task.status, Task.StatusChoices.OPEN)
        self.assertEqual(task.user, self.user)
    
    def test_task_timestamp(self):
        """
        Test that timestamp is auto-generated and cannot be modified
        """
        task = Task.objects.create(
            user=self.user,
            title='Timestamp Test',
            description='Checking timestamp behavior'
        )
        
        # Check timestamp is auto-generated
        self.assertIsNotNone(task.timestamp)
        
        # Verify timestamp is close to current time
        time_diff = timezone.now() - task.timestamp
        self.assertTrue(time_diff < timedelta(seconds=1))
    
    def test_task_status_choices(self):
        """
        Test all possible status choices
        """
        status_choices = [
            Task.StatusChoices.OPEN,
            Task.StatusChoices.WORKING,
            Task.StatusChoices.PENDING_REVIEW,
            Task.StatusChoices.COMPLETED,
            Task.StatusChoices.OVERDUE,
            Task.StatusChoices.CANCELLED
        ]
        
        for status in status_choices:
            task = Task.objects.create(
                user=self.user,
                title=f'Task with status {status}',
                description='Status test',
                status=status
            )
            self.assertEqual(task.status, status)
    
    def test_task_tags(self):
        """
        Test adding tags to a task
        """
        task = Task.objects.create(
            user=self.user,
            title='Tagged Task',
            description='Task with tags'
        )
        task.tags.add(self.tag)
        
        # Check tag association
        self.assertEqual(list(task.tags.all()), [self.tag])
        self.assertEqual(task.tags.count(), 1)
    
    def test_task_due_date(self):
        """
        Test optional due date functionality
        """
        future_date = timezone.now() + timedelta(days=7)
        
        task = Task.objects.create(
            user=self.user,
            title='Future Task',
            description='Task with due date',
            due_date=future_date
        )
        
        self.assertEqual(task.due_date, future_date)

class TagModelTest(TestCase):
    def test_tag_creation(self):
        """
        Test tag creation and uniqueness
        """
        tag = Tag.objects.create(name='Unique Tag')
        
        # Check tag creation
        self.assertTrue(isinstance(tag, Tag))
        self.assertEqual(tag.name, 'Unique Tag')
        
        # Test unique constraint
        with self.assertRaises(Exception):
            Tag.objects.create(name='Unique Tag')
