<template>
  <div class="home-page">
    <div class="bg-image"></div>

    <div class="overlay">
      <div class="auth-box">
        <button
          @click="isAdmin = !isAdmin"
          class="toggle-btn"
        >
          Switch to {{ isAdmin ? "User" : "Admin" }} Mode
        </button>

        <LoginForm
          v-if="!showRegister"
          :isAdmin="isAdmin"
          @toggle-mode="isAdmin = !isAdmin"
        />

        <div v-if="!showRegister" class="switch-link">
          <a @click="showRegister = true">
            Don't have an account? Register
          </a>
        </div>

        <RegisterForm v-else />

        <div v-if="showRegister" class="switch-link">
          <a @click="showRegister = false">
            Already have an account? Login
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import LoginForm from "../components/LoginForm.vue";
import RegisterForm from "../components/RegisterForm.vue";

export default {
  components: { LoginForm, RegisterForm },
  setup() {
    const showRegister = ref(false);
    const isAdmin = ref(false);
    return { showRegister, isAdmin };
  },
};
</script>

<style scoped>
.home-page {
  position: relative;
  min-height: 100vh;
  overflow-y: hidden;
}

.bg-image {
  position: fixed;
  inset: 0;
  background-image: url("/images/parking-hero.jpg");
  background-size: cover;
  background-position: center;
  z-index: -1;
}

.overlay {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.auth-box {
  width: 100%;
  max-width: 380px;
}

.toggle-btn {
  width: 100%;
  margin-bottom: 16px;
  padding: 8px 16px;
  background: black;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.switch-link {
  text-align: center;
  margin-top: 12px;
}

.switch-link a {
  cursor: pointer;
  color: white;
  text-decoration: underline;
}
</style>
