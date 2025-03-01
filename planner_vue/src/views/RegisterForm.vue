<template>
    <div>
        <!-- Menu Bar for navigation -->
        <nav class="menu-bar">
            <button @click="goToLogin">Login</button> <!-- Navigates to the login page -->
        </nav>

        <h2>Register</h2>
        <div class="register-card">
            <form @submit.prevent="registerUser">
                <!-- Username Input Field -->
                <div>
                    <label for="username">Username</label>
                    <input type="text" id="username" v-model="username" required />
                    <p v-if="errors.username" style="color: red;">{{ errors.username }}</p>
                </div>
                
                <!-- Email Input Field -->
                <div>
                    <label for="email">Email</label>
                    <input type="email" id="email" v-model="email" required />
                    <p v-if="errors.email" style="color: red;">{{ errors.email }}</p>
                </div>
                
                <!-- Password Input Field -->
                <div>
                    <label for="password">Password</label>
                    <input type="password" id="password" v-model="password" required />
                    <p v-if="errors.password" style="color: red;">{{ errors.password }}</p>
                </div>
                
                <!-- Password Confirmation Field -->
                <div>
                    <label for="password2">Password Confirmation</label>
                    <input type="password" id="password2" v-model="password2" required />
                    <p v-if="errors.password2" style="color: red;">{{ errors.password2 }}</p>
                    <p v-if="errors.non_field_errors" style="color: red;">{{ errors.non_field_errors }}</p>
                </div>
                
                <!-- Submit Button -->
                <div>
                    <button type="submit" class="button">Register</button>
                </div>
            </form>
            
            <!-- Displays error messages if registration fails -->
            <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
        </div>
    </div>
</template>
  
<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { API_BASE_URL } from '../config.js';

// Reactive variables for form inputs and errors
const username = ref('');
const email = ref('');
const password = ref('');
const password2 = ref('');
const errorMessage = ref('');
const errors = ref({
    username: '',
    email: '',
    password: '',
    password2: '',
    non_field_errors: ''
});
const router = useRouter();

// Function to handle user registration
const registerUser = async () => {
    // Reset error messages before submitting
    errors.value = {
        username: '',
        email: '',
        password: '',
        password2: '',
        non_field_errors: ''
    };

    try {
        // Send a POST request to the registration API
        const response = await axios.post(`${API_BASE_URL}/register/`, {
            username: username.value,
            email: email.value,
            password: password.value,
            password2: password2.value,
        });

        // Redirects to the main page if registration is successful
        if (response.status === 201) {
            router.push('/');
        }
    } catch (error) {
        // Handles backend validation errors
        if (error.response && error.response.data) {
            const backendErrors = error.response.data;

            // Assigns error messages from backend to respective form fields
            if (backendErrors.username) {
                errors.value.username = backendErrors.username[0];
            }
            if (backendErrors.email) {
                errors.value.email = backendErrors.email[0];
            }
            if (backendErrors.password) {
                errors.value.password = backendErrors.password[0];
            }
            if (backendErrors.password2) {
                errors.value.password2 = backendErrors.password2[0];
            }
            if (backendErrors.non_field_errors) {
                errors.value.non_field_errors = backendErrors.non_field_errors[0];
            }
            errorMessage.value = 'Registration failed. Please fix the errors above.';
        } else {
            errorMessage.value = 'An error occurred. Please try again later.';
        }
        console.error(error);
    }
};

// Redirects user to the main page
const goToLogin = () => {
    window.location.href = '/';
};
</script>
  
<style scoped>
/* Menu Bar Styling */
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

/* Register Button Styling */
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

.button:hover {
    background: #36976a;
    color: white;
}

/* Register Card Styling */
.register-card {
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

/* Input Field Styling */
input, textarea, select {
    width: calc(100% - 20px);
    padding: 8px;
    margin-top: 15px;
    margin-bottom: 10px;
    border-radius: 5px;
    border: 1px solid #ddd;
    font-size: 14px;
}

textarea {
    height: 80px;
    resize: none;
}
</style>
