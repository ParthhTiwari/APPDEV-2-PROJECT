<template>
  <div class="register-card">
    <h2 class="title">Register</h2>

    <form @submit.prevent="handleRegister">
      <div class="field">
        <label>Full Name</label>
        <input
          v-model="form.name"
          type="text"
          placeholder="Enter your full name"
          required
        />
      </div>

      <div class="field">
        <label>Email</label>
        <input
          v-model="form.email"
          type="email"
          placeholder="Enter your email"
          required
        />
      </div>

      <div class="field">
        <label>Password</label>
        <input
          v-model="form.password"
          type="password"
          placeholder="Enter password (min 6 chars)"
          minlength="6"
          required
        />
      </div>

      <div class="field">
        <label>Confirm Password</label>
        <input
          v-model="form.confirmPassword"
          type="password"
          placeholder="Confirm password"
          required
        />
        <p
          v-if="form.password && form.confirmPassword && form.password !== form.confirmPassword"
          class="error-text"
        >
          Passwords do not match
        </p>
      </div>

      <button
        type="submit"
        class="submit-btn"
        :disabled="loading || form.password !== form.confirmPassword"
      >
        {{ loading ? "Registering..." : "Register" }}
      </button>
    </form>

    <p v-if="error" class="message error">{{ error }}</p>
    <p v-if="success" class="message success">{{ success }}</p>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { authAPI } from "../services/api";

export default {
  setup() {
    const router = useRouter();
    const loading = ref(false);
    const error = ref("");
    const success = ref("");

    const form = ref({
      name: "",
      email: "",
      password: "",
      confirmPassword: "",
    });

    const handleRegister = async () => {
      if (form.value.password !== form.value.confirmPassword) {
        error.value = "Passwords do not match!";
        return;
      }

      if (form.value.password.length < 6) {
        error.value = "Password must be at least 6 characters!";
        return;
      }

      loading.value = true;
      error.value = "";
      success.value = "";

      try {
        const response = await authAPI.register({
          name: form.value.name,
          email: form.value.email,
          password: form.value.password,
        });

        success.value =
          response.data.message ||
          "Registration successful! Redirecting to login...";

        form.value = {
          name: "",
          email: "",
          password: "",
          confirmPassword: "",
        };

        setTimeout(() => {
          router.push("/");
        }, 2000);
      } catch (err) {
        error.value =
          err.response?.data?.error ||
          "Registration failed. Please try again.";
      } finally {
        loading.value = false;
      }
    };

    return {
      form,
      loading,
      error,
      success,
      handleRegister,
    };
  },
};
</script>

<style scoped>
.register-card {
  max-width: 400px;
  margin: 0 auto;
  padding: 24px;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.title {
  text-align: center;
  margin-bottom: 20px;
}

.field {
  margin-bottom: 14px;
  display: flex;
  flex-direction: column;
}

.field label {
  font-size: 14px;
  margin-bottom: 4px;
}

.field input {
  padding: 8px 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 14px;
}

.submit-btn {
  width: 100%;
  padding: 10px;
  margin-top: 8px;
  border: none;
  border-radius: 4px;
  background: black;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

.submit-btn:disabled {
  background: #9fbbe5;
  cursor: not-allowed;
}

.error-text {
  color: #d9534f;
  font-size: 12px;
  margin-top: 4px;
}

.message {
  margin-top: 12px;
  font-size: 14px;
}

.message.error {
  color: #d9534f;
}

.message.success {
  color: #28a745;
}

.divider {
  margin: 20px 0;
}

.login-link {
  text-align: center;
  font-size: 14px;
}
</style>
