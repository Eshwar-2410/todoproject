import os
import sys
import django
from django.core.wsgi import get_wsgi_application

# Add the project directory to Python path
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

# Initialize Django
get_wsgi_application()

from django.contrib.auth.models import User

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpass123')
    print("Superuser created successfully!")
else:
    print("Superuser already exists.")
