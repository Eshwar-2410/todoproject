# Todo API

## Overview
Django-based Todo List API with comprehensive task management and authentication.

## Features
- User Authentication
- Task CRUD Operations
- Admin Interface
- REST API Endpoints

## CI/CD Status
![Django CI](https://github.com/yourusername/todo-api/workflows/Django%20CI/badge.svg)
[![codecov](https://codecov.io/gh/yourusername/todo-api/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/todo-api)

## Documentation
[View Documentation](https://yourusername.github.io/todo-api)

## Setup
1. Clone the repository
2. Create virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python myproject/manage.py migrate`
5. Create superuser: `python myproject/manage.py createsuperuser`
6. Run server: `python myproject/manage.py runserver`

## Testing
Run tests with: `python myproject/manage.py test todos.tests`

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit changes
4. Push to the branch
5. Create pull request

## License
MIT License

## Todo API Authentication Setup

## Creating a Superuser

To use the API with Basic Authentication, you need to create a superuser:

```bash
python myproject/manage.py createsuperuser
```

Follow the prompts to create a user. For the Postman collection, you'll need to use the credentials you create here.

## Authentication Details

- **Authentication Type**: Basic Authentication
- **Authentication Method**: Username and Password
- **Default Credentials in Postman Collection**: 
  - Username: admin
  - Password: admin123 (CHANGE THIS IMMEDIATELY)

## Postman Collection Usage

1. Import the `Todo_API_Postman_Collection.json` file into Postman
2. Update the Basic Authentication credentials with your created superuser credentials
3. Ensure the Django server is running (`python myproject/manage.py runserver`)

## Security Recommendations

1. Always use HTTPS in production
2. Change default credentials immediately
3. Use strong, unique passwords
4. Consider implementing token-based authentication for more secure access
