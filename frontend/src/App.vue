<template>
  <div id="app">
    <!-- Header -->
    <header>
      <div class="header-content">
        <h1>Audio Transcription Service</h1>
      </div>
      <!-- Health Status Indicator -->
      <div class="health-status">
        <span :class="['status-dot', { 'up': isServerUp, 'down': !isServerUp }]"></span>
        <span>{{ statusMessage }}</span>
      </div>
    </header>

    <!-- Main Content -->
    <main>
      <FileUpload @upload-files="handleUploadedFiles" />

      <div class="action-buttons">
        <QueryTranscription @search="handleSearch" />
        <button class="get-all-button" @click="fetchTranscriptions">
          Get All Transcriptions
        </button>
      </div>

      <div v-if="searchMessage" class="search-message">
        {{ searchMessage }}
      </div>

      <TranscriptionList :transcriptions="transcriptions" />
    </main>

    <!-- Footer -->
    <footer>
      <div class="footer-content">
        <p>© 2025 Audio Transcription Service. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import FileUpload from './components/FileUpload.vue';
import QueryTranscription from './components/QueryTranscription.vue';
import TranscriptionList from './components/TranscriptionList.vue';

// axios.defaults.baseURL = '/api';
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
axios.defaults.baseURL = apiUrl;
console.log('API URL:', apiUrl);  // Check if the correct API URL is being set

// Transcription data and search
const transcriptions = ref([]);
const searchQuery = ref('');

// Health status
const isServerUp = ref(false);
const statusMessage = ref('Checking server status...');

// Fetch transcriptions from the backend
const fetchTranscriptions = async () => {
  try {
    const response = await axios.get('/transcriptions');
    transcriptions.value = response.data;
    searchQuery.value = ''; // Clear the search query
  } catch (error) {
    console.error('Error fetching transcriptions:', error);
  }
};


// Handle file uploads
const handleUploadedFiles = async (files) => {

  const formData = new FormData();
  Array.from(files).forEach(file => formData.append('files', file, file.name));


  try {
    // const response = await axios.post('/transcribe', formData);
    const response = await axios.post('/transcribe', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    transcriptions.value = response.data.transcriptions; // Update transcriptions

  } catch (error) {
    console.error('Error uploading files:', error);
  }
};

const searchMessage = ref('');

const handleSearch = async (query) => {
  searchQuery.value = query;

  // If the search query is empty, do nothing
  if (!query.trim()) {
    searchMessage.value = '';
    return;
  }

  try {
    const response = await axios.get('/search', {
      params: { file_name: query },
    });

    // Check if the response contains the "No transcriptions found" message
    if (response.data.message && response.data.message === "No transcriptions found matching the criteria") {
      // Clear the transcriptions list and show a message to the user
      transcriptions.value = [];
      searchMessage.value = 'No transcriptions found matching your search criteria.';
    } else {
      // Update transcriptions with search results
      transcriptions.value = response.data;
      searchMessage.value = '';
    }
  } catch (error) {
    console.error('Error searching transcriptions:', error);
    searchMessage.value = 'An error occurred while searching for transcriptions.';
  }
};

// Check backend health
const checkHealth = async () => {
  try {
    const response = await axios.get('/health');
    if (response.status === 200) {
      isServerUp.value = true;
      statusMessage.value = 'Server is up';
    } else {
      isServerUp.value = false;
      statusMessage.value = 'Server is down';
    }
  } catch (error) {
    isServerUp.value = false;
    statusMessage.value = 'Server is down';
    console.error('Health check failed:', error);
  }
};

// Automatically fetch transcriptions and check health when the component is mounted
onMounted(() => {
  fetchTranscriptions();
  checkHealth();
});
</script>

<style>
/* Blueish Theme */
:root {
  --primary-blue: #3498db;
  --secondary-blue: #5dade2;
  --background-blue: #f0f8ff;
  --text-dark: #2c3e50;
  --white: #ffffff;
  --shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  --green-up: #2ecc71;
  --red-down: #e74c3c;
}

body {
  margin: 0;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  background-color: var(--background-blue);
  color: var(--text-dark);
}

#app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Header */
header {
  background: linear-gradient(135deg, var(--primary-blue), var(--secondary-blue));
  padding: 2rem;
  border-radius: 10px;
  margin-bottom: 1.5rem;
  box-shadow: var(--shadow);
  position: relative;
  width: 100%;
}
header h1 {
  font-size: 2.5rem;
  color: var(--white); /* Reverted back to white */
  margin: 0;
  text-align: center;
}

/* Health Status Indicator */
.health-status {
  position: absolute;
  bottom: 0.5rem;
  right: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.2); /* Semi-transparent background */
  padding: 0.25rem 0.5rem;
  border-radius: 5px;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
}

.status-dot.up {
  background-color: var(--green-up);
}

.status-dot.down {
  background-color: var(--red-down);
}

.health-status span {
  color: var(--text-dark); /* Darker color for better readability */
  font-size: 0.9rem;
}

/* Main Content */
main {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem;
  width: 100%; /* Ensure it takes full width */
  max-width: 1200px; /* Constrain the width of the main content */
  margin: 0 auto; /* Center the main content */
}

/* Group Search and Get All Transcriptions Button */
.action-buttons {
  display: flex;
  gap: 1rem;
  align-items: center;
}

/* Style for both buttons */
.action-buttons button,
.action-buttons .query-transcription-button {
  background-color: var(--primary-blue);
  color: var(--white);
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
  height: 40px; /* Ensure consistent height */
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-buttons button:hover,
.action-buttons .query-transcription-button:hover {
  background-color: var(--secondary-blue);
}

.search-message {
  color: var(--red-down);
  margin-top: 1rem;
  font-size: 0.9rem;
}

/* Footer */
footer {
  background: var(--white);
  padding: 1rem;
  margin-top: auto;
  border-top: 1px solid var(--background-blue);
  text-align: center;
  width: 100%; 
}

footer p {
  margin: 0;
  color: var(--text-dark);
}


</style>