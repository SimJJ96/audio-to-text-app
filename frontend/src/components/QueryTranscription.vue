<template>
  <div class="search-bar">
    <div class="search-input-wrapper">
      <input
        v-model="searchQuery"
        @keyup.enter="performSearch"
        placeholder="Search by file name..."
        class="search-input"
      />
      <span v-if="searchQuery" class="clear-icon" @click="clearSearch">×</span>
    </div>
    <button @click="performSearch">Search</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const searchQuery = ref('');
const emit = defineEmits(['search']);

const performSearch = () => {
  if (searchQuery.value.trim()) {
    emit('search', searchQuery.value);
  }
};

const clearSearch = () => {
  searchQuery.value = '';
  emit('search', '');
};
</script>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-input-wrapper {
  position: relative;
  flex: 1;
}

.search-input {
  width: 100%;
  padding: 0.75rem;
  padding-right: 40px; /* Add padding to prevent text overlap with clear icon */
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  border-color: #3498db;
}

.clear-icon {
  position: absolute;
  right: 10px; /* Adjust this value to align the icon properly */
  top: 50%;
  transform: translateY(-50%);
  color: #666;
  cursor: pointer;
  font-size: 1.5rem;
  padding: 0 8px;
}

.clear-icon:hover {
  color: #333;
}
</style>