<template>
    <div>
        <h2>Login</h2>
        <div class="login-card">
            <form @submit.prevent="handleLogin">
                <!-- Username input field -->
                <input v-model="username" type="text" placeholder="Username" required />
                
                <!-- Password input field -->
                <input v-model="password" type="password" placeholder="Password" required />
                
                <!-- Submit button to trigger login function -->
                <button type="submit" class="button">Login</button>
                
                <!-- Register Button -->
                <router-link to="/register">
                    <button type="button" class="button">Register</button>
                </router-link>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { API_BASE_URL } from '../config.js';

// Reactive state variables for username and password
const username = ref(''); // Stores the inputted username
const password = ref(''); // Stores the inputted password

// Vue Router instance for handling navigation
const router = useRouter();

// Function to handle user login
const handleLogin = async () => {
    try {
        // Send login request to the backend API
        const response = await axios.post(`${API_BASE_URL}/token/`, {
            username: username.value,
            password: password.value
        });

        // Store received access and refresh tokens in local storage
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);

        // Redirect the user to the tasks page upon successful login
        router.push('/tasks'); 
    } catch (error) {
        console.error("Login failed", error);
        alert('Invalid credentials or server error');
    }
};
</script>

<style scoped>
/* Styling for the login button */
.button {
    background: #42b983;
    color: white;
    border: none;
    padding: 5px 10px;
    margin-right: 20px;
    margin-left: 20px;
    cursor: pointer;
    border-radius: 3px;
}

/* Change button color on hover */
.button:hover {
    background: #36976a;
    color: white;
}

/* Card styling for the login form container */
.login-card {
    background: #f9f9f9;
    padding: 15px;
    margin: 10px 0;
    border: 1px solid #ddd;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.3s ease;
    max-width: 500px;
    position: relative;
    margin-top: 60px;
}

/* Input field styling for username and password */
input, textarea, select {
    width: calc(100% - 20px);
    padding: 8px;
    margin-top: 15px;
    margin-bottom: 10px;
    border-radius: 5px;
    border: 1px solid #ddd;
    font-size: 14px;
}

/* Styling for textareas (if needed in future) */
textarea {
    height: 80px;
    resize: none;
}
</style>
