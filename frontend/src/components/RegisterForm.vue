<!-- filepath: frontend/src/components/RegisterForm.vue -->
<template>
  <div class="card shadow">
    <div class="card-body p-5">
      <h2 class="card-title text-center mb-4">📝 Register</h2>
      
      <form @submit.prevent="handleRegister">
        <div class="mb-3">
          <label class="form-label">Full Name</label>
          <input 
            v-model="form.name" 
            type="text" 
            class="form-control"
            placeholder="Enter your full name"
            required
          >
        </div>
        
        <div class="mb-3">
          <label class="form-label">Email</label>
          <input 
            v-model="form.email" 
            type="email" 
            class="form-control"
            placeholder="Enter your email"
            required
          >
        </div>
        
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input 
            v-model="form.password" 
            type="password" 
            class="form-control"
            placeholder="Enter password (min 6 chars)"
            minlength="6"
            required
          >
        </div>
        
        <div class="mb-3">
          <label class="form-label">Confirm Password</label>
          <input 
            v-model="form.confirmPassword" 
            type="password" 
            class="form-control"
            placeholder="Confirm password"
            required
          >
          <small v-if="form.password && form.confirmPassword && form.password !== form.confirmPassword" class="text-danger">
            ❌ Passwords do not match
          </small>
        </div>
        
        <button 
          type="submit" 
          class="btn btn-primary w-100" 
          :disabled="loading || form.password !== form.confirmPassword"
        >
          {{ loading ? 'Registering...' : 'Register' }}
        </button>
      </form>
      
      <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
      <div v-if="success" class="alert alert-success mt-3">{{ success }}</div>
      
      <hr class="my-4">
      <p class="text-center">
        Already registered? 
        <router-link to="/" class="text-decoration-none">
          Login here
        </router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { authAPI } from '../services/api';

export default {
  setup() {
    const router = useRouter();
    const loading = ref(false);
    const error = ref('');
    const success = ref('');
    
    const form = ref({
      name: '',
      email: '',
      password: '',
      confirmPassword: ''
    });
    
    const handleRegister = async () => {
      // Validation
      if (form.value.password !== form.value.confirmPassword) {
        error.value = 'Passwords do not match!';
        return;
      }
      
      if (form.value.password.length < 6) {
        error.value = 'Password must be at least 6 characters!';
        return;
      }
      
      loading.value = true;
      error.value = '';
      success.value = '';
      
      try {
        const response = await authAPI.register({
          name: form.value.name,
          email: form.value.email,
          password: form.value.password
        });
        
        success.value = response.data.message || 'Registration successful! Redirecting to login...';
        
        // Reset form
        form.value = { name: '', email: '', password: '', confirmPassword: '' };
        
        // Redirect after 2 seconds
        setTimeout(() => {
          router.push('/');
        }, 2000);
        
      } catch (err) {
        error.value = err.response?.data?.error || 'Registration failed. Please try again.';
      } finally {
        loading.value = false;
      }
    };
    
    return {
      form,
      loading,
      error,
      success,
      handleRegister
    };
  }
};
</script>

<style scoped>
.card {
  border: none;
  border-radius: 10px;
}

small {
  display: block;
  margin-top: 5px;
}
</style>