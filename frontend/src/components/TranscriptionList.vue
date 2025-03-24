<template>
  <div class="transcription-list">
    <h2>Transcriptions</h2>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>File Name</th>
            <th>Transcription</th>
            <th>Created Time</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="transcription in transcriptions" :key="transcription.id">
            <td>{{ transcription.file_name }}</td>
            <td>{{ transcription.text }}</td>
            <td>{{ transcription.created_at }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
defineProps({
  transcriptions: {
    type: Array,
    required: true,
  },
});
</script>

<style scoped>
.transcription-list {
  margin-top: 2rem;
  width: 100%;
}

.table-container {
  max-width: 800px; /* Constrain the width */
  width: 100%; /* Ensure it takes full width of its container */
  max-height: 400px; /* Set a fixed height for vertical scrolling */
  overflow-y: auto; /* Make it scrollable vertically */
  border: 1px solid #ddd; /* Optional: Add a border for better visibility */
  border-radius: 8px; /* Optional: Add rounded corners */
}

table {
  width: 100%; /* Ensure the table takes full width of its container */
  border-collapse: collapse;
}

th,
td {
  padding: 0.75rem;
  border: 1px solid #ddd;
  text-align: left;
}

th {
  background-color: #f4f4f4;
  font-weight: bold;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f1f1f1;
}
</style>