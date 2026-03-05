<template>
  <patient-nav />
  <div class="container mt-4">
    <router-view />
  </div>
</template>

<script setup lang="ts">
import PatientNav from './PatientNav.vue';
</script>