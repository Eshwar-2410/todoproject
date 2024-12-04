from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class TodoE2ETest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up WebDriver for E2E testing
        """
        super().setUpClass()
        
        # Setup Chrome WebDriver
        service = Service(ChromeDriverManager().install())
        cls.selenium = webdriver.Chrome(service=service)
        cls.selenium.implicitly_wait(10)
    
    def setUp(self):
        """
        Create test user and login
        """
        # Create test user
        self.user = User.objects.create_superuser(
            username='admin', 
            email='admin@example.com', 
            password='adminpass123'
        )
    
    def login(self):
        """
        Helper method to log in via Django admin
        """
        self.selenium.get(f'{self.live_server_url}/admin/login/')
        username_input = self.selenium.find_element(By.ID, 'id_username')
        password_input = self.selenium.find_element(By.ID, 'id_password')
        submit_button = self.selenium.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
        
        username_input.send_keys('admin')
        password_input.send_keys('adminpass123')
        submit_button.click()
        
        # Wait for dashboard to load
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, 'content'))
        )
    
    def test_create_todo_item(self):
        """
        E2E test for creating a todo item
        """
        self.login()
        
        # Navigate to Todo app
        self.selenium.get(f'{self.live_server_url}/admin/todos/task/add/')
        
        # Fill out task creation form
        title_input = self.selenium.find_element(By.ID, 'id_title')
        description_input = self.selenium.find_element(By.ID, 'id_description')
        status_select = self.selenium.find_element(By.ID, 'id_status')
        
        title_input.send_keys('E2E Test Task')
        description_input.send_keys('Task created via Selenium E2E test')
        
        # Select status
        for option in status_select.find_elements(By.TAG_NAME, 'option'):
            if option.text == 'Open':
                option.click()
                break
        
        # Submit form
        submit_button = self.selenium.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
        submit_button.click()
        
        # Verify task creation
        success_message = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'success'))
        )
        self.assertIn('was added successfully', success_message.text)
    
    def test_view_todo_items(self):
        """
        E2E test for viewing todo items
        """
        # Create a test task first
        task = Task.objects.create(
            user=self.user,
            title='View Test Task',
            description='Task for viewing test',
            status=Task.StatusChoices.OPEN
        )
        
        self.login()
        
        # Navigate to Todo list view
        self.selenium.get(f'{self.live_server_url}/admin/todos/task/')
        
        # Wait for task list to load
        task_list = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'results'))
        )
        
        # Check if our test task is in the list
        task_rows = task_list.find_elements(By.TAG_NAME, 'tr')
        task_found = any('View Test Task' in row.text for row in task_rows)
        self.assertTrue(task_found)
    
    def test_update_todo_item(self):
        """
        E2E test for updating a todo item
        """
        # Create a test task first
        task = Task.objects.create(
            user=self.user,
            title='Update Test Task',
            description='Task for update test',
            status=Task.StatusChoices.OPEN
        )
        
        self.login()
        
        # Navigate to task edit page
        self.selenium.get(f'{self.live_server_url}/admin/todos/task/{task.id}/change/')
        
        # Update task details
        title_input = self.selenium.find_element(By.ID, 'id_title')
        description_input = self.selenium.find_element(By.ID, 'id_description')
        status_select = self.selenium.find_element(By.ID, 'id_status')
        
        title_input.clear()
        title_input.send_keys('Updated Task Title')
        
        description_input.clear()
        description_input.send_keys('Updated task description')
        
        # Select new status
        for option in status_select.find_elements(By.TAG_NAME, 'option'):
            if option.text == 'Completed':
                option.click()
                break
        
        # Submit form
        submit_button = self.selenium.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
        submit_button.click()
        
        # Verify update success
        success_message = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'success'))
        )
        self.assertIn('was changed successfully', success_message.text)
    
    def test_delete_todo_item(self):
        """
        E2E test for deleting a todo item
        """
        # Create a test task first
        task = Task.objects.create(
            user=self.user,
            title='Delete Test Task',
            description='Task for delete test',
            status=Task.StatusChoices.OPEN
        )
        
        self.login()
        
        # Navigate to task delete page
        self.selenium.get(f'{self.live_server_url}/admin/todos/task/{task.id}/delete/')
        
        # Confirm deletion
        confirm_button = self.selenium.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
        confirm_button.click()
        
        # Verify deletion success
        success_message = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'success'))
        )
        self.assertIn('was deleted successfully', success_message.text)
    
    @classmethod
    def tearDownClass(cls):
        """
        Close WebDriver after tests
        """
        cls.selenium.quit()
        super().tearDownClass()
