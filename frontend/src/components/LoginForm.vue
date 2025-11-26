<!-- filepath: frontend/src/components/LoginForm.vue -->
<script>
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { authAPI, adminAPI } from '../services/api';

export default {
  props: {
    isAdmin: {
      type: Boolean,
      default: false
    }
  },

  emits: ['toggle-mode'],

  setup(props, { emit }) {
    const router = useRouter();
    const loading = ref(false);
    const error = ref('');

    // Credentials
    const credentials = ref({
      email: '',
      password: ''
    });

    // Watch admin toggle → Auto-fill admin login
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

    // Login handler
    const handleLogin = async () => {
      loading.value = true;
      error.value = '';

      try {
        if (props.isAdmin) {
          // Admin Login
          const response = await adminAPI.dashboard(
            credentials.value.email,
            credentials.value.password
          );

          // Store admin token
          if (response.data.token) {
            localStorage.setItem('auth_token', response.data.token);
          }
          
          localStorage.setItem('admin_email', credentials.value.email);
          localStorage.setItem('admin_password', credentials.value.password);
          localStorage.setItem('user_role', 'admin');
          localStorage.setItem('is_admin', 'true');

          router.push('/admin/dashboard');
        } else {
          // User Login
          const response = await authAPI.login(credentials.value);

          const { user_id, is_admin, token } = response.data;

          // Store user token
          if (token) {
            localStorage.setItem('auth_token', token);
          }
          
          localStorage.setItem('user_id', user_id);
          localStorage.setItem('user_role', 'user');
          localStorage.setItem('is_admin', is_admin || false);

          router.push('/user/dashboard');
        }
      } catch (err) {
        error.value =
          err.response?.data?.error || 'Login failed. Please try again.';
      } finally {
        loading.value = false;
      }
    };

    return {
      credentials,
      loading,
      error,
      handleLogin
    };
  }
};
</script>