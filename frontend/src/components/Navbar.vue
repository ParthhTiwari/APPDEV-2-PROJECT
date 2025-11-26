<!-- filepath: frontend/src/components/Navbar.vue -->
<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow">
    <div class="container">
      <!-- Brand -->
      <router-link to="/" class="navbar-brand fw-bold">
        🅿️ Parking App
      </router-link>

      <!-- Toggle for mobile -->
      <button 
        class="navbar-toggler" 
        type="button" 
        data-bs-toggle="collapse" 
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Menu -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <!-- Admin Menu -->
          <li v-if="isAdmin" class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
              ⚙️ Admin
            </a>
            <ul class="dropdown-menu">
              <li>
                <router-link to="/admin/dashboard" class="dropdown-item">
                  📊 Dashboard
                </router-link>
              </li>
              <li>
                <router-link to="/admin/create-lot" class="dropdown-item">
                  ➕ Create Lot
                </router-link>
              </li>
              <li>
                <router-link to="/admin/lots" class="dropdown-item">
                  🏢 Manage Lots
                </router-link>
              </li>
              <li><hr class="dropdown-divider"></li>
              <li>
                <a @click="logout" class="dropdown-item cursor-pointer">
                  🚪 Logout
                </a>
              </li>
            </ul>
          </li>

          <!-- User Menu -->
          <li v-else-if="isLoggedIn" class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
              👤 {{ userName }}
            </a>
            <ul class="dropdown-menu">
              <li>
                <router-link to="/user/dashboard" class="dropdown-item">
                  🏠 Dashboard
                </router-link>
              </li>
              <li>
                <router-link to="/user/history" class="dropdown-item">
                  📜 Parking History
                </router-link>
              </li>
              <li>
                <router-link to="/user/export" class="dropdown-item">
                  📥 Export Data
                </router-link>
              </li>
              <li><hr class="dropdown-divider"></li>
              <li>
                <a @click="logout" class="dropdown-item cursor-pointer">
                  🚪 Logout
                </a>
              </li>
            </ul>
          </li>

          <!-- Guest Menu -->
          <li v-else class="nav-item">
            <router-link to="/" class="nav-link">
              🔓 Login / Register
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    const isAdmin = ref(false);
    const isLoggedIn = ref(false);
    const userName = ref('');

    onMounted(() => {
      // Check if user is logged in
      const adminEmail = localStorage.getItem('admin_email');
      const userId = localStorage.getItem('user_id');

      if (adminEmail) {
        isAdmin.value = true;
        isLoggedIn.value = true;
      } else if (userId) {
        isLoggedIn.value = true;
        userName.value = localStorage.getItem('user_name') || 'User';
      }
    });

    const logout = () => {
      localStorage.clear();
      isAdmin.value = false;
      isLoggedIn.value = false;
      router.push('/');
    };

    return {
      isAdmin,
      isLoggedIn,
      userName,
      logout
    };
  }
};
</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}

.navbar {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>