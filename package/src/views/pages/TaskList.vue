<template>
    <v-card elevation="10">
      <v-card-item class="pa-6">
        <v-card-title class="text-h5 pt-sm-2 pb-7">Task List</v-card-title>
  
        <!-- Create Task Button -->
        <v-btn class="mb-4" color="green" @click="openCreateDialog">Create Task</v-btn>
  
        <v-table class="task-table">
          <thead>
            <tr>
              <th class="text-subtitle-1 font-weight-bold">Id</th>
              <th class="text-subtitle-1 font-weight-bold">Title</th>
              <th class="text-subtitle-1 font-weight-bold">Description</th>
              <th class="text-subtitle-1 font-weight-bold">Completed</th>
              <th class="text-subtitle-1 font-weight-bold">Created At</th>
              <th class="text-subtitle-1 font-weight-bold">Due Date</th>
              <th class="text-subtitle-1 font-weight-bold">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="taskItem in tasks" :key="taskItem.id">
              <td><p class="text-15 font-weight-medium">{{ taskItem.id }}</p></td>
              <td><h6 class="text-subtitle-1 font-weight-bold">{{ taskItem.title }}</h6></td>
              <td><p class="text-body-1">{{ taskItem.description || 'N/A' }}</p></td>
              <td>
                <div :class="taskItem.completed ? 'badge bg-success' : 'badge bg-danger'">
                  {{ taskItem.completed ? 'Yes' : 'No' }}
                </div>
              </td>
              <td><h6 class="text-body-1">{{ new Date(taskItem.created_at).toLocaleDateString() }}</h6></td>
              <td><h6 class="text-body-1">{{ taskItem.due_date ? new Date(taskItem.due_date).toLocaleDateString() : 'N/A' }}</h6></td>
              <td>
                <v-btn class="btn btn-primary" @click="openEditDialog(taskItem)">Edit</v-btn>
                <v-btn class="btn btn-danger" @click="deleteTask(taskItem.id)">Delete</v-btn>
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-card-item>
  
      <!-- Create Task Dialog -->
      <v-dialog v-model="showCreateDialog" max-width="600px">
        <v-card>
          <v-card-title>
            <span class="text-h5">Create Task</span>
          </v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="valid" lazy-validation>
              <v-text-field v-model="newTask.title" label="Title" :rules="[rules.required]"></v-text-field>
              <v-textarea v-model="newTask.description" label="Description" :rules="[rules.required]"></v-textarea>
              <v-checkbox v-model="newTask.completed" label="Completed"></v-checkbox>
  
              <!-- Native HTML Date Picker for Due Date -->
               <label for=""> Due Date</label>
              <input
                type="date"
                v-model="newTask.due_date"
                class="native-date-picker form-control"
                style="border:none; outline:none;"
              />
              <!-- <v-text-field label="Due Date">
                <template #append>
                </template>
              </v-text-field> -->
  
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn color="green" @click="createTask">Create</v-btn>
            <v-btn @click="closeCreateDialog">Cancel</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
  
      <!-- Edit Task Dialog -->
      <v-dialog v-model="showDialog" max-width="600px">
        <v-card>
          <v-card-title>
            <span class="text-h5">Edit Task</span>
          </v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="valid" lazy-validation>
              <v-text-field v-model="task.title" label="Title" :rules="[rules.required]"></v-text-field>
              <v-textarea v-model="task.description" label="Description" :rules="[rules.required]"></v-textarea>
              <v-checkbox v-model="task.completed" label="Completed"></v-checkbox>
  
              <!-- Native HTML Date Picker for Due Date -->
              <v-text-field label="Due Date">
                <template #append>
                  <input
                    type="date"
                    v-model="task.due_date"
                    class="native-date-picker"
                    style="border:none; outline:none;"
                  />
                </template>
              </v-text-field>
  
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn color="green" @click="updateTask">Update</v-btn>
            <v-btn @click="closeDialog">Cancel</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
  
      <!-- Snackbar for Toast Notifications -->
      <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000">
        {{ snackbarMessage }}
        <template #action>
          <v-btn color="white" text @click="snackbar = false">Close</v-btn>
        </template>
      </v-snackbar>
    </v-card>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { format } from 'date-fns'; // Import a date formatting utility
  
  const tasks = ref([]);
  const showDialog = ref(false);
  const showCreateDialog = ref(false);
  const selectedTaskId = ref(null);
  const task = ref({
    id: 0,
    title: '',
    description: null,
    completed: false,
    created_at: '',
    due_date: null,
  });
  const newTask = ref({
    title: '',
    description: '',
    completed: false,
    due_date: null,
  });
  const valid = ref(false);
  
  const snackbar = ref(false);
  const snackbarMessage = ref('');
  const snackbarColor = ref('success');
  
  const rules = {
    required: (value) => !!value || 'Required.',
  };
  
  // Date formatting function
  const formatDate = (date) => {
    if (!date) return '';
    return format(new Date(date), 'yyyy-MM-dd'); // Use the 'date-fns' library to format the date
  };
  
  const fetchTasks = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/drf/task/');
      tasks.value = response.data;
    } catch (error) {
      console.error('Error fetching tasks:', error);
    }
  };
  
  // Open dialog to create task
  const openCreateDialog = () => {
    newTask.value = {
      title: '',
      description: '',
      completed: false,
      due_date: null,
    };
    showCreateDialog.value = true;
  };
  
  const closeCreateDialog = () => {
    showCreateDialog.value = false;
  };
  
  const createTask = async () => {
    if (!newTask.value.title || !newTask.value.description) {
      snackbarMessage.value = 'Please fill out all required fields.';
      snackbarColor.value = 'error';
      snackbar.value = true;
      return;
    }
  
    try {
      await axios.post('http://127.0.0.1:8000/drf/task/', newTask.value);
      snackbarMessage.value = 'Task created successfully!';
      snackbarColor.value = 'success';
      snackbar.value = true;
      closeCreateDialog();
      fetchTasks(); // Refresh the task list
    } catch (error) {
      console.error('Error creating task:', error);
      snackbarMessage.value = 'Failed to create task.';
      snackbarColor.value = 'error';
      snackbar.value = true;
    }
  };
  
  const openEditDialog = (taskData) => {
    task.value = { ...taskData };
    selectedTaskId.value = taskData.id;
    showDialog.value = true;
  };
  
  const closeDialog = () => {
    showDialog.value = false;
    task.value = {
      id: 0,
      title: '',
      description: null,
      completed: false,
      created_at: '',
      due_date: null,
    };
    selectedTaskId.value = null;
  };
  
  const updateTask = async () => {
    if (!task.value) return;
    try {
      await axios.patch(`http://127.0.0.1:8000/drf/task/update/${selectedTaskId.value}/`, task.value);
      snackbarMessage.value = 'Task updated successfully!';
      snackbarColor.value = 'success';
      snackbar.value = true;
      closeDialog();
      fetchTasks();
    } catch (error) {
      console.error('Error updating task:', error);
      snackbarMessage.value = 'Failed to update task.';
      snackbarColor.value = 'error';
      snackbar.value = true;
    }
  };
  
  const deleteTask = async (taskId) => {
    const confirmDelete = confirm('Are you sure you want to delete this task?');
    if (!confirmDelete) return;
  
    try {
      await axios.delete(`http://127.0.0.1:8000/drf/task/delete/${taskId}/`);
      snackbarMessage.value = 'Task deleted successfully!';
      snackbarColor.value = 'success';
      snackbar.value = true;
      fetchTasks();
    } catch (error) {
      console.error('Error deleting task:', error);
      snackbarMessage.value = 'Failed to delete task.';
      snackbarColor.value = 'error';
      snackbar.value = true;
    }
  };
  
  onMounted(() => {
    fetchTasks();
  });
  </script>
  