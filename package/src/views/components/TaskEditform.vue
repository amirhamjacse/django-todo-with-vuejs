<!-- TaskEditForm.vue -->
<template>
    <v-dialog v-model="showDialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h5">Edit Task</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-text-field
              v-model="task.title"
              label="Title"
              :rules="[rules.required]"
            ></v-text-field>
            <v-textarea
              v-model="task.description"
              label="Description"
              :rules="[rules.required]"
            ></v-textarea>
            <v-checkbox
              v-model="task.completed"
              label="Completed"
            ></v-checkbox>
            <v-menu
              v-model="dueDatePicker"
              :close-on-content-click="false"
              transition="scale-transition"
              offset-y
              min-width="290px"
            >
              <template #activator="{ props }">
                <v-text-field
                  v-model="task.due_date"
                  label="Due Date"
                  readonly
                  v-bind="props"
                ></v-text-field>
              </template>
              <v-date-picker v-model="task.due_date" @input="dueDatePicker = false"></v-date-picker>
            </v-menu>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn color="green" @click="updateTask">Update</v-btn>
          <v-btn @click="showDialog = false">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue';
  import axios from 'axios';
  
  const props = defineProps<{
    taskId: number;
    taskData: any; // You can define a more specific type based on your task structure
    showDialog: boolean;
    onClose: () => void;
  }>();
  
  const task = ref({ ...props.taskData });
  const dueDatePicker = ref(false);
  const valid = ref(false);
  
  const rules = {
    required: (value: any) => !!value || 'Required.',
  };
  
  const updateTask = async () => {
    try {
      const response = await axios.patch(`http://127.0.0.1:8000/drf/task/update/${props.taskId}/`, task.value);
      console.log(response.data);
      props.onClose(); // Close the dialog after successful update
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };
  </script>
  