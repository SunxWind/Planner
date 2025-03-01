import { createRouter, createWebHistory } from 'vue-router';  // Import necessary functions from Vue Router
import RegisterForm from '@/views/RegisterForm.vue';  // Import the RegisterForm component for user registration
import LoginView from '@/views/LoginView.vue';  // Import the LoginView component for user login
import DashboardView from '@/views/DashboardView.vue';  // Import the DashboardView component for authenticated users
import TaskList from '@/views/TaskList.vue';  // Import the TaskList component for task management
import AuthService from '@/services/AuthService';  // Import AuthService to manage authentication state

// Define application routes
const routes = [
    {
        path: '/register', // URL path for user registration
        name: 'register', // Route name for easy reference
        component: RegisterForm // Component to render for this route
    },
    {
        path: '/', // Root URL path, serves as the login page
        name: 'login', // Route name for easy reference
        component: LoginView // Component to render for this route
    },
    {
        path: '/dashboard', // URL path for the dashboard
        name: 'dashboard', // Route name for easy reference
        component: DashboardView, // Component to render for this route
        meta: { requiresAuth: true } // Indicates that authentication is required to access this page
    },
    {
        path: '/tasks', // URL path for the task list
        name: 'tasks', // Route name for easy reference
        component: TaskList, // Component to render for this route
        meta: { requiresAuth: true } // Indicates that authentication is required to access this page
    },
];

// Create Vue Router instance
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL), // Use HTML5 history mode for cleaner URLs
    routes, // Assign the defined routes to the router instance
});

// Navigation Guard to check authentication before accessing protected routes
router.beforeEach((to, from, next) => {
    // If the route requires authentication and the user is not authenticated
    if (to.meta.requiresAuth && !AuthService.isAuthenticated()) {
        next('/login'); // Redirect user to the login page
    } else {
        next(); // Allow navigation to the requested route
    }
});

export default router; // Export the router instance for use in the Vue app
