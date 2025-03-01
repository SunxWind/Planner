<template>
    <div>
        <!-- Menu Bar -->
        <nav class="menu-bar">
            <!-- Navigation buttons -->
            <button @click="startCreatingTask">New Task</button>
            <button @click="goToDashboard">Dashboard</button>
            <button @click="logout">Logout</button>
        </nav>

        <!-- Filter Section for task statuses -->
        <div class="multiselect-container">
            <label for="multiselect">Filter:</label>
            <div class="multiselect-wrapper" @click="toggleDropdown">
                <div class="selected-options">
                    <span v-if="selectedOptions.length === 0">Select Statuses...</span>
                    <span 
                        v-for="option in selectedOptions" 
                        :key="option" 
                        class="selected-item"
                    >
                        {{ option }} ✖
                    </span>
                </div>
                <!-- Dropdown for selecting status filters -->
                <div class="dropdown" v-if="isOpen">
                    <div 
                        v-for="option in options" 
                        :key="option" 
                        @click.stop="toggleOption(option)" 
                        :class="['dropdown-item', { selected: selectedOptions.includes(option) }]"
                    >
                        <input type="checkbox" :checked="selectedOptions.includes(option)" />
                        {{ option }}
                    </div>
                </div>
            </div>
        </div>

        <div class="grid-container">
            <!-- Display message if there are no tasks -->
            <div v-if="tasks.length === 0" class="no-tasks">
                You do not have tasks yet...
            </div>
            
            <!-- Task Creation Card -->
            <div v-if="creatingTask" class="task-card">
                <!-- Input fields for new task details -->
                <input v-model="newTask.title" placeholder="Title" required />
                <textarea v-model="newTask.description" placeholder="Description" required></textarea>
                
                <!-- Status selection dropdown -->
                <div class="task-status">
                    <label>Status:</label>
                </div>    
                <select v-model="newTask.status">
                    <option value="In queue">In queue</option>
                    <option value="In progress">In progress</option>
                    <option value="Completed">Completed</option>
                    <option value="Postponed">Postponed</option>
                </select>

                <!-- Creation date selection -->
                <div class="task-date">
                    <label>Created:</label>
                    <input type="date" v-model="newTask.creation_date" :max="currentDate" required />
                </div>    
                
                <!-- Buttons to save or cancel task creation -->
                <div class="task-edit-buttons">
                    <button @click="saveNewTask" class="save-btn">Create task</button>
                    <button @click="cancelCreatingTask" class="cancel-btn">Cancel</button>
                </div>
            </div>

            <!-- Task List -->
            <div
                v-for="task in filteredTasks"
                :key="task.id"
                :class="['task-card', { expanded: editingTaskId === task.id }]"
                @click="toggleTask(task.id)"
            >
                <!-- Delete button for each task -->
                <div class="task-actions">
                    <button @click.stop="deleteTask(task.id)">🗑️</button>
                </div>
                
                <!-- Title field, editable when task is in edit mode -->
                <div>
                    <h3 v-if="editingTaskId !== task.id">{{ task.title }}</h3>
                    <input
                        v-else
                        v-model="task.title"
                        placeholder="Title"
                        class="title-input"
                        required
                    />
                </div>

                <!-- Task description, expandable when clicked -->
                <p v-if="editingTaskId !== task.id">
                    {{ expandedTask === task.id ? task.description : getShortDescription(task.description) }}
                </p>
                <textarea
                    v-else
                    v-model="task.description"
                    placeholder="Description"
                    required
                ></textarea>

                <!-- Status selection dropdown when editing -->
                <div v-if="editingTaskId === task.id" class="task-status">
                    <label>Status:</label>
                    <select v-model="task.status">
                        <option value="In queue">In queue</option>
                        <option value="In progress">In progress</option>
                        <option value="Completed">Completed</option>
                        <option value="Postponed">Postponed</option>
                    </select>
                </div>
                <div v-else class="task-status">
                    <label>Status:</label> {{ task.status }}
                </div>

                <!-- Task creation date, editable when task is in edit mode -->
                <div class="task-date">
                    <label>Created:</label>
                    <span v-if="editingTaskId !== task.id">{{ task.creation_date }}</span>
                    <input
                        v-else
                        type="date"
                        v-model="task.creation_date"
                        class="edit-date"
                    />
                </div>

                <!-- Save and Cancel buttons when editing a task -->
                <div v-if="editingTaskId === task.id" class="task-edit-buttons">
                    <button @click.stop="saveTask(task)" class="save-btn">Save</button>
                    <button @click.stop="cancelEdit" class="cancel-btn">Cancel</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';
import { API_BASE_URL } from '../config.js';

// Reactive state variables
const tasks = ref([]); // Stores the list of tasks
const expandedTask = ref(null); // Stores the ID of the currently expanded task
const editingTaskId = ref(null); // Stores the ID of the task being edited
const creatingTask = ref(false); // Boolean to track if a new task is being created
const selectedOptions = ref([]);  // Stores the selected filter options
const currentDate = ref(new Date().toISOString().split('T')[0]); // Stores the current date
const isOpen = ref(false); // Tracks if the dropdown menu is open
const options = ref(["In queue", "In progress", "Completed", "Postponed"]); // Possible task statuses

// Toggles the dropdown menu for filtering tasks
const toggleDropdown = () => {
    isOpen.value = !isOpen.value;
};

// Adds or removes a selected filter option
const toggleOption = (option) => {
    if (selectedOptions.value.includes(option)) {
        // If option is already selected, remove it
        selectedOptions.value = selectedOptions.value.filter(o => o !== option);
    } else {
        // Otherwise, add it to the selected filters
        selectedOptions.value.push(option);
    }
    // Save the selected filter options to local storage
    localStorage.setItem('selectedFilters', JSON.stringify(selectedOptions.value));
};

// Closes the dropdown if a user clicks outside of it
const closeDropdown = (event) => {
    if (!event.target.closest('.multiselect-container')) {
        isOpen.value = false;
    }
};

// Computed property to filter tasks based on selected statuses
// Ensures tasks with the same status remain grouped together
const filteredTasks = computed(() => {
    // If no tasks exist, return an empty array
    if (!tasks.value.length) return [];

    let filtered = selectedOptions.value.length === 0 
        // Show all tasks if no filter is selected
        ? tasks.value
        // Otherwise, filter tasks by selected statuses
        : tasks.value.filter(task => selectedOptions.value.includes(task.status));

    // Sort tasks so that those with the same status appear together
    return filtered.sort((a, b) => options.value.indexOf(a.status) - options.value.indexOf(b.status));
});

// Fetches tasks from the API
const fetchTasks = async () => {
    try {
        // Make the GET request with both Authorization and CSRF token headers
        const response = await axios.get(`${API_BASE_URL}/tasks/`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
        });

        // Store fetched tasks in the reactive state
        tasks.value = response.data;
    } catch (error) {
        console.error('Error fetching tasks', error);
        alert('Failed to load tasks.');
    }
};

// Reactive object for storing new task details
const newTask = ref({
    title: '',
    description: '',
    status: 'In queue',
    creation_date: currentDate.value,
});

// Starts the task creation process
const startCreatingTask = () => {
    creatingTask.value = true;
};

// Cancels task creation and resets the input fields
const cancelCreatingTask = () => {
    creatingTask.value = false;
    newTask.value = { title: '', description: '', status: 'In queue', creation_date: currentDate.value };
};

// Sends a request to create a new task and updates the task list
const saveNewTask = async () => {
    try {
        const response = await axios.post(`${API_BASE_URL}/tasks/create/`, newTask.value, {
            headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
        });
        // Add the newly created task to the task list
        tasks.value.push(response.data);
        // Reset the input fields
        newTask.value = { title: '', description: '', status: 'In queue', creation_date: currentDate.value };
        // Hide the creation form
        creatingTask.value = false;
    } catch (error) {
        console.error('Error saving task', error);
        alert('Failed to save task.');
    }
};

// Shortens long task descriptions for display purposes
const getShortDescription = (description) => {
    return description.length > 100 ? description.slice(0, 100) + '...' : description;
};

// Expands or collapses a task and enables editing mode
const toggleTask = (taskId) => {
    expandedTask.value = taskId;
    editingTaskId.value = taskId;
};

// Cancels editing and refreshes the task list
const cancelEdit = () => {
    expandedTask.value = null;
    editingTaskId.value = null;
    fetchTasks(); // Reload the tasks to discard unsaved changes
};

// Saves task changes by sending an update request to the API
const saveTask = async (task) => {
    try {
        await axios.put(`${API_BASE_URL}/tasks/${task.id}/`, task, {
            headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
        });
        alert('Task updated successfully!');
        editingTaskId.value = null;
        expandedTask.value = null;
        // Refresh the task list
        fetchTasks();
    } catch (error) {
        console.error('Error saving task', error);
        alert('Failed to save task.');
    }
};

// Deletes a task after user confirmation
const deleteTask = async (taskId) => {
    if (!confirm('Are you sure you want to delete this task?')) return;

    try {
        // Send the DELETE request with both Authorization and CSRF token headers
        await axios.delete(`${API_BASE_URL}/tasks/delete/${taskId}/`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
        });

        // Remove the deleted task from the list
        tasks.value = tasks.value.filter((task) => task.id !== taskId);
    } catch (error) {
        console.error('Error deleting task', error);
        alert('Failed to delete task.');
    }
};

// Redirects to the dashboard page
const goToDashboard = () => {
    window.location.href = '/dashboard';
};

// Logs out the user by clearing stored data and redirecting to the login page
const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('selectedFilters'); // Clear saved filter settings
    axios.defaults.headers.common['Authorization'] = null;
    window.location.href = '/';
};

// Runs when the component is mounted
onMounted(() => {
    if (!localStorage.getItem('access_token')) {
        // Redirect to main page if no access token is found
        router.push('/');
    } else {
        // Load tasks from API
        fetchTasks();
        // Close dropdown when clicking outside
        document.addEventListener('click', closeDropdown);

        // Load saved filters from local storage
        const savedFilters = localStorage.getItem('selectedFilters');
        selectedOptions.value = savedFilters ? JSON.parse(savedFilters) : options.value;
    }
});

// Watches for changes in the selected filter options and updates local storage
watch(selectedOptions, (newOptions) => {
    localStorage.setItem('selectedFilters', JSON.stringify(newOptions));
}, { deep: true });
</script>


<style scoped>
/* Menu Bar */
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

.menu-bar button:hover {
    background: #36976a;
    color: white;
}

/* Message if no tasks exist */
.no-tasks {
    color: #888;
    display: inline-flex;
    align-content: baseline;
    justify-content: baseline;
    font-style: italic;
    margin-top: 10px;
    margin-bottom: 20px;
}

/* Container for task cards */
.grid-container {
  width: inherit;  
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 20px;
  padding: 16px;
  justify-content: center;
}

.task-card {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  flex: 1 1 200px; /* Responsive base size */
  max-width: 200px;
}

.task-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* Task expanded for editing */
.task-card.expanded {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80%;
  height: auto;
  max-width: 600px;
  z-index: 1000;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* Trash-button for deletion of a task */
.task-actions {
    position: absolute;
    top: 5px;
    right: 5px;
    margin-bottom: 50px;
    z-index: 1;
}

.task-actions button {
    background: none;
    border: none;
    font-size: 18px;
    cursor: pointer;
    margin-left: 5px;
}

.task-status,
.task-date {
    margin-top: 10px;
    font-size: 14px;
}

.task-status label,
.task-date label {
    font-weight: bold;
    margin-right: 5px;
}

/* Buttons in the expanded task card */
.task-edit-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
}

.save-btn {
    background: #42b983;
    color: white;
    border: none;
    padding: 5px 10px;
    cursor: pointer;
    border-radius: 3px;
}

.cancel-btn {
    background: red;
    color: white;
    border: none;
    padding: 5px 10px;
    cursor: pointer;
    border-radius: 3px;
}

button:hover {
    opacity: 0.8;
}

/* Input Styling */
.title-input {
    width: calc(100% - 20px);
    padding: 8px;
    margin-top: 40px;
    margin-bottom: 10px;
    border-radius: 5px;
    border: 1px solid #ddd;
    font-size: 14px;
}

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

/* Tasks' filter styles */
.multiselect-container {
    position: sticky;
    top: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    position: relative;
}

.multiselect-container label {
    font-weight: bold;
    white-space: nowrap;
}

.multiselect-wrapper {
    width: 400px;
    min-height: 25px;
    min-width: 200px;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 8px;
    cursor: pointer;
    background-color: white;
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    align-items: center;
}

.selected-options {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    font-size: 14px;
}

.selected-item {
    background: #42b983;
    color: white;
    padding: 3px 8px;
    border-radius: 3px;
    font-size: 12px;
    cursor: pointer;
}

.dropdown {
    position: absolute;
    top: 35px;
    left: auto;
    width: 150px;
    justify-content: right;
    align-items: flex-start;
    background: white;
    border: 1px solid #ddd;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    margin-top: 5px;
    z-index: 10;
}

.dropdown-item {
    width: auto;
    padding: 8px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-items: left;
    gap: 10px;
    transition: background 0.3s ease;
}

.dropdown-item input {
    cursor: pointer;
    width: 20px;
}

.dropdown-item:hover {
    background: #42b983;
    color: white;
}

.selected {
    background: #42b983;
    color: white;
}
</style>
