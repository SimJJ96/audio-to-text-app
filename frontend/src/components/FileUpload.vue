<template>
  <div class="file-upload">
    <h2>Upload Audio File</h2>
    <input type="file" @change="handleFileUpload" multiple />
    <button @click="uploadFiles" :disabled="!isValid || loading">Upload</button>
    <p v-if="message" :class="{ error: isError }">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const emit = defineEmits(['upload-files']);
const files = ref([]);
const message = ref('');
const isError = ref(false);
const loading = ref(false);

const MAX_FILES = 5;  

const isValid = computed(() => files.value.length > 0 && !isError.value);

const handleFileUpload = (event) => {
  files.value = event.target.files;
  message.value = '';
  isError.value = false;

  // Check if the number of files exceeds the limit
  if (files.value.length > MAX_FILES) {
    message.value = `You can upload a maximum of ${MAX_FILES} files at once.`;
    isError.value = true;
    files.value = [];
    return;
  }

  for (const file of files.value) {
    if (!isValidFileFormat(file)) {
      message.value = 'Invalid file format. Supported formats: .wav, .mp3, .mp4, .m4a, .webm.';
      isError.value = true;
      files.value = [];
      return;
    }
  }

  message.value = 'Files are valid and ready to upload.';
};

const isValidFileFormat = (file) => {
  const supportedFormats = ['audio/wav', 'audio/mpeg', 'audio/mp3', 'audio/mp4', 'audio/m4a', 'audio/webm'];
  return supportedFormats.includes(file.type.toLowerCase());
};

const uploadFiles = () => {
  if (files.value.length === 0) {
    message.value = 'No files selected.';
    isError.value = true;
    return;
  }

  loading.value = true;
  message.value = 'Loading...';

  setTimeout(() => {
    emit('upload-files', files.value);
    loading.value = false; 
    message.value = 'Files uploaded and transcribed successfully'; 
  }, 2000); 
};
</script>

<style scoped>
.file-upload {
  margin-bottom: 2rem;
}

.file-upload input[type="file"] {
  margin-bottom: 1rem;
}

.file-upload button {
  padding: 0.5rem 1rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.file-upload button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.file-upload p {
  margin-top: 1rem;
}

.file-upload .error {
  color: #e74c3c;
}
</style>
