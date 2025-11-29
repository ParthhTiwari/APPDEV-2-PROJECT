
<template>
  <Navbar v-if="showNavbar" />
  
  <main class="container mt-4">
    <router-view />
  </main>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import Navbar from './components/Navbar.vue';

const route = useRoute();

const showNavbar = computed(() => {
  return route.name !== 'Login' && route.name !== 'Register';
});
</script>

<style>
body {
  background-color: #f5f5f5;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

main {
  max-width: 2000px;
  margin: 0 auto;
}
</style>
