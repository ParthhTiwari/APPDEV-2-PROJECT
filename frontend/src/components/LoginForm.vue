<template>
  <form @submit.prevent="handleLogin" style="max-width:350px; margin:auto; padding:40px; border:1px solid #ccc; border-radius:8px; background:white;">
    <h2 style="text-align:center; margin-bottom:22px;">{{ isAdmin ? "Admin Login" : "User Login" }}</h2>
    <div style="margin-bottom:12px; ">
      <label>Email:</label>
      <input 
        v-model="credentials.email" 
        type="email" 
        required 
        placeholder="Email"
        style="width:100%; padding:8px; margin-top:4px; border-radius:4px; border:1px solid #ccc;"
      />
    </div>
    <div style="margin-bottom:12px; ">
      <label>Password:</label>
      <input 
        v-model="credentials.password" 
        type="password" 
        required 
        placeholder="Password"
        style="width:100%; padding:8px; margin-top:4px; padding:8px; margin-top:4px; border-radius:4px; border:1px solid #ccc;"
      />
    </div>
    <button 
      type="submit" 
      :disabled="loading"
      style="width:100%; padding:10px; background:black; color:white; border:none; border-radius:4px; cursor:pointer;"
    >
      {{ loading ? "Logging in..." : "Login" }}
    </button>
    <div v-if="error" style="color:red; margin-top:12px;">{{ error }}</div>
  </form>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { authAPI, adminAPI } from '../services/api';

const props = defineProps({
  isAdmin: {
    type: Boolean,
    default: false
  }
});
const emit = defineEmits(['toggle-mode']);

const router = useRouter();
const loading = ref(false);
const error = ref('');
const credentials = ref({ email: '', password: '' });

watch(
  () => props.isAdmin,
  (isAdminMode) => {
    if (isAdminMode) {
      credentials.value.email = "admin@gmail.com";
      credentials.value.password = "admin123";
    } else {
      credentials.value.email = "";
      credentials.value.password = "";
    }
  },
  { immediate: true }
);

const handleLogin = async () => {
  loading.value = true;
  error.value = '';

  try {
    if (props.isAdmin) {
      const response = await adminAPI.dashboard(
        credentials.value.email,
        credentials.value.password
      );
      if (response.data.token) {
        localStorage.setItem('auth_token', response.data.token);
      }
      localStorage.setItem('admin_email', credentials.value.email);
      localStorage.setItem('admin_password', credentials.value.password);
      localStorage.setItem('user_role', 'admin');
      localStorage.setItem('is_admin', 'true');
      router.push('/admin/dashboard');
    } else {
      const response = await authAPI.login(credentials.value);
      const { user_id, is_admin, token } = response.data;
      if (token) {
        localStorage.setItem('auth_token', token);
      }
      localStorage.setItem('user_id', user_id);
      localStorage.setItem('user_role', 'user');
      localStorage.setItem('is_admin', is_admin || false);
      router.push('/user/dashboard');
    }
  } catch (err) {
    error.value = err.response?.data?.error || 'Login failed. Please try again.';
  } finally {
    loading.value = false;
  }
};
</script>
