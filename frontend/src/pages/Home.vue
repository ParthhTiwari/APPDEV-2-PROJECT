<!-- filepath: frontend/src/pages/Home.vue -->
<template>
  <div class="min-vh-100 d-flex align-items-center" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-5">
          <!-- Login Form -->
          <LoginForm 
            v-if="!showRegister" 
            :isAdmin="isAdmin"
            @toggle-mode="isAdmin = !isAdmin"
          />
          
          <!-- Register Form -->
          <RegisterForm v-else />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import LoginForm from '../components/LoginForm.vue';
import RegisterForm from '../components/RegisterForm.vue';

export default {
  components: {
    LoginForm,
    RegisterForm
  },
  
  setup() {
    const showRegister = ref(false);
    const isAdmin = ref(false);
    
    return {
      showRegister,
      isAdmin
    };
  }
};
</script>