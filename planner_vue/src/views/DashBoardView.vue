<template>
    <!-- Displays dashboard data if available -->
    <div v-if="dashboardData">
        <!-- Menu Bar for navigation -->
        <nav class="menu-bar">
            <button @click="goToTasks">Tasks</button> <!-- Navigates to the tasks page -->
            <button @click="logout">Logout</button> <!-- Logs out the user -->
        </nav>

        <!-- Displays a welcome message from dashboard data -->
        <h1>{{ dashboardData.message }}</h1>
        <div>
            <h3>User Information</h3>
            <!-- Displays the logged-in user's username and email -->
            <p>Username: {{ dashboardData.user_info.username }}</p>
            <p>Email: {{ dashboardData.user_info.email }}</p>
        </div>
    </div>
    <!-- Shows a loading message while fetching data -->
    <div v-else>
        <p>Loading...</p>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { API_BASE_URL } from '../config.js';

// Reactive state variables
const dashboardData = ref(null); // Stores fetched dashboard data
const router = useRouter(); // Initializes the router for navigation

// Fetches dashboard data from the API
const fetchDashboardData = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/dashboard/`, {
            headers: {
                // Includes authentication token in the request
                Authorization: `Bearer ${localStorage.getItem('access_token')}`
            }
        });
        // Stores response data in the reactive variable
        dashboardData.value = response.data;
    } catch (error) {
        console.error("Error fetching dashboard data", error);
        // Redirects the user to the main page if the token is invalid or expired
        router.push('/');
    }
};

// Calls fetchDashboardData when the component is mounted
onMounted(() => {
    fetchDashboardData();
});

// Logs out the user by removing tokens and redirecting to the login page
const logout = () => {
    // Clears the access token
    localStorage.removeItem('access_token');
    // Clears the refresh token
    localStorage.removeItem('refresh_token');
    // Redirects to the main page
    window.location.href = '/';
};

// Redirects user to the tasks page
const goToTasks = () => {
    window.location.href = '/tasks';
};
</script>
  
<style scoped>
/* Styles for the menu bar */
.menu-bar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background: #42b983;
    padding: 10px 20px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
    z-index: 1000;
}

/* Styling for menu buttons */
.menu-bar button {
    background: white;
    color: #42b983;
    border: none;
    padding: 8px 15px;
    cursor: pointer;
    border-radius: 5px;
    font-weight: bold;
    transition: background 0.3s ease;
}

/* Button hover effect */
.menu-bar button:hover {
    background: #36976a;
    color: white;
}

/* Styles for dashboard container */
.dashboard {
    text-align: center;
    padding: 20px;
}
</style>
