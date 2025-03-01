# Planner Project

## Overview

The Planner project is a web application that allows users to manage tasks. It consists of a backend built with Django and a frontend built with Vue.js.

## Project Structure

```
Planner
├─ planner
│  ├─ accounts
│  │  ├─ apps.py
│  │  ├─ serializers.py
│  │  ├─ urls.py
│  │  ├─ views.py
│  │  ├─ __init__.py
│  │  └─ __pycache__
│  │     ├─ apps.cpython-311.pyc
│  │     ├─ serializers.cpython-311.pyc
│  │     ├─ urls.cpython-311.pyc
│  │     ├─ views.cpython-311.pyc
│  │     └─ __init__.cpython-311.pyc
│  ├─ planner
│  │  ├─ asgi.py
│  │  ├─ serializers.py
│  │  ├─ settings.py
│  │  ├─ urls.py
│  │  ├─ views.py
│  │  ├─ wsgi.py
│  │  ├─ __init__.py
│  │  └─ __pycache__
│  │     ├─ wsgi.cpython-311.pyc
│  │     └─ __init__.cpython-311.pyc
│  ├─ viewer
│  │  ├─ admin.py
│  │  ├─ apps.py
│  │  ├─ migrations
│  │  │  ├─ 0001_initial.py
│  │  │  ├─ 0002_task_short_description.py
│  │  │  ├─ 0003_remove_task_short_description.py
│  │  │  ├─ __init__.py
│  │  │  └─ __pycache__
│  │  │     ├─ 0001_initial.cpython-311.pyc
│  │  │     ├─ 0002_task_short_description.cpython-311.pyc
│  │  │     ├─ 0003_remove_task_short_description.cpython-311.pyc
│  │  │     └─ __init__.cpython-311.pyc
│  │  ├─ models.py
│  │  ├─ static
│  │  ├─ __init__.py
│  └─ __init__.py
├─ planner_vue
│  ├─ dist
│  │  ├─ assets
│  │  │  ├─ index-B3PIpKdi.js
│  │  │  └─ index-DXtFDItX.css
│  │  ├─ index.html
│  │  └─ vite.svg
│  ├─ index.html
│  ├─ package-lock.json
│  ├─ package.json
│  ├─ public
│  │  └─ vite.svg
│  ├─ src
│  │  ├─ App.vue
│  │  ├─ assets
│  │  │  └─ vue.svg
│  │  ├─ components
│  │  │  └─ HelloWorld.vue
│  │  ├─ config.js
│  │  ├─ main.js
│  │  ├─ router
│  │  │  └─ index.js
│  │  ├─ services
│  │  │  └─ AuthService.js
│  │  ├─ style.css
│  │  └─ views
│  │     ├─ DashBoardView.vue
│  │     ├─ LoginView.vue
│  │     ├─ RegisterForm.vue
│  │     └─ TaskList.vue
│  └─ vite.config.js
├─ DB_Diagram_Planner.drawio
├─ package-lock.json
├─ package.json
├─ README.md
└─ requirements.txt

```
## Backend (Django)

### Installation

1. Clone the repository.
2. Navigate to the planner directory.
3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```sh
   python manage.py migrate
   ```
5. Run the development server:
   ```sh
   python manage.py runserver
   ```

### Applications

#### Accounts

- **Views**: API views for login, registration, and user information.
- **Serializers**: Serializers for user registration and authentication.
- **URLs**: URL patterns for the accounts API.

#### Viewer

- **Models**: Task management.

#### Здфттук

- **Views**: API views for task creation, retrieval, update, and deletion.
- **Serializers**: Serializers for task management.
- **URLs**: URL patterns for the viewer API.

### Settings

The settings for the Django project are configured in settings.py. This includes database configuration, installed applications, middleware, and other settings.

### URLs

The URL patterns for the Django project are defined in urls.py. This includes routes for the admin interface and the API endpoints.

## Frontend (Vue.js)

### Installation

1. Navigate to the planner_vue directory.
2. Install the required packages:
   ```sh
   npm install
   ```
3. Run the development server:
   ```sh
   npm run dev
   ```

### Components

- **HelloWorld.vue**: A sample component to demonstrate Vue.js functionality.

### Views

- **RegisterForm.vue**: A view for user registration.
- **LoginView.vue**: A view for user login.
- **DashboardView.vue**: A view for displaying user dashboard.
- **TaskList.vue**: A view for displaying and managing tasks.

### Router

The router configuration is defined in index.js. This includes routes for registration, login, dashboard, and task management.

### Services

- **AuthService.js**: A service for handling authentication-related API calls.

### Configuration

The API base URL is configured in config.js.

## Deployment

### Backend

To deploy the Django backend, follow the standard deployment process for Django applications. This includes setting up a production database, configuring the web server, and applying migrations.

### Frontend

To build the Vue.js frontend for production, use the following command:
```sh
npm run build
```
This will generate the production-ready files in the `dist` directory.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with a descriptive message.
4. Push your changes to your fork.
5. Create a pull request to the main repository.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

For any questions or inquiries, please contact the project maintainer at [mr.symonov@gmail.ru](mailto:mr.symonov@gmail.com).

---