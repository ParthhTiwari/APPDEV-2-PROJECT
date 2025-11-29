<template>
  <nav
    style="
      background:black;
      color:white;
      padding:10px 0;
      box-shadow:0 2px 4px;
      border-bottom:2px solid #333;
      border-radius:20px;
      position:sticky;
      top:0;
      z-index:10;
    "
  >
    <div
      style="
        max-width:1900px;
        margin:auto;
        display:flex;
        align-items:center;
        justify-content:space-between;
        padding:0 20px;
      "
    >
      <!-- Brand -->
      <router-link
        to="/"
        style="
          font-weight:bold;
          color:white;
          font-size:1.3rem;
          text-decoration:none;
          border-radius:26px;
          padding:8px 26px;
          border:2px solid;
          background:black;
        "
      >
        Parking App
      </router-link>

      <!-- Menu -->
      <ul
        style="
          margin:0;
          padding:0;
          list-style:none;
          display:flex;
          align-items:center;
          gap:24px;
        "
      >
        <!-- Admin Menu -->
        <li v-if="isAdmin" style="position:relative;">
          <div
            @click.stop="toggleAdminDropdown"
            style="cursor:pointer; user-select:none; padding:8px 18px;"
          >
            ⚙️ Admin ▼
          </div>
          <ul
            v-if="showAdminDropdown"
            style="
              position:absolute;
              background:white;
              color:#333;
              top:38px;
              right:0;
              min-width:170px;
              border-radius:6px;
              box-shadow:0 4px 16px rgba(0,0,0,0.11);
              padding:10px 0;
              z-index:20;
            "
          >
            <li>
              <router-link
                to="/admin/dashboard"
                style="display:block; padding:8px 22px; color:inherit; text-decoration:none;"
              >📊 Dashboard</router-link>
            </li>
            <li>
              <router-link
                to="/admin/create-lot"
                style="display:block; padding:8px 22px; color:inherit; text-decoration:none;"
              >➕ Create Lot</router-link>
            </li>
            <li>
              <router-link
                to="/admin/lots"
                style="display:block; padding:8px 22px; color:inherit; text-decoration:none;"
              >🏢 Manage Lots</router-link>
            </li>
            <li><hr style="margin:6px 0;" /></li>
            <li>
              <a
                @click="logout"
                style="display:block; padding:8px 22px; color:inherit; text-decoration:none; cursor:pointer;"
              >🚪 Logout</a>
            </li>
          </ul>
        </li>

        <!-- User Menu -->
        <li v-else-if="isLoggedIn" style="position:relative;">
          <div
            @click.stop="toggleUserDropdown"
            style="cursor:pointer; user-select:none; padding:8px 18px;"
          >
            👤 {{ userName || 'User' }} ▼
          </div>
          <ul
            v-if="showUserDropdown"
            style="
              position:absolute;
              background:white;
              color:#333;
              top:38px;
              right:0;
              min-width:170px;
              border-radius:6px;
              box-shadow:0 4px 16px rgba(0,0,0,0.11);
              padding:10px 0;
              z-index:20;
            "
          >
            <li>
              <router-link
                to="/user/dashboard"
                style="display:block; padding:8px 22px; color:inherit; text-decoration:none;"
              >🏠 Dashboard</router-link>
            </li>
            <li>
              <router-link
                to="/user/history"
                style="display:block; padding:8px 22px; color:inherit; text-decoration:none;"
              >📜 Parking History</router-link>
            </li>
            <li>
              <router-link
                to="/user/export"
                style="display:block; padding:8px 22px; color:inherit; text-decoration:none;"
              >📥 Export Data</router-link>
            </li>
            <li><hr style="margin:6px 0;" /></li>
            <li>
              <a
                @click="logout"
                style="display:block; padding:8px 22px; color:inherit; text-decoration:none; cursor:pointer;"
              >🚪 Logout</a>
            </li>
          </ul>
        </li>

        <!-- Guest Menu -->
        <li v-else>
          <router-link
            to="/"
            style="color:white; text-decoration:none; font-weight:500;"
          >
            🔓 Login / Register
          </router-link>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
import { ref, onMounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";

export default {
  setup() {
    const router = useRouter();
    const route = useRoute();

    const isAdmin = ref(false);
    const isLoggedIn = ref(false);
    const userName = ref("");
    const showAdminDropdown = ref(false);
    const showUserDropdown = ref(false);

    const updateAuthState = () => {
      const adminEmail = localStorage.getItem("admin_email");
      const userId = localStorage.getItem("user_id");

      if (adminEmail) {
        isAdmin.value = true;
        isLoggedIn.value = true;
        userName.value = adminEmail;
      } else if (userId) {
        isAdmin.value = false;
        isLoggedIn.value = true;
        userName.value = localStorage.getItem("user_name") || "User";
      } else {
        isAdmin.value = false;
        isLoggedIn.value = false;
        userName.value = "";
      }
    };

    watch(
      () => route.fullPath,
      () => updateAuthState()
    );

    onMounted(() => {
      updateAuthState();
      window.addEventListener("click", () => {
        showAdminDropdown.value = false;
        showUserDropdown.value = false;
      });
    });

    const toggleAdminDropdown = () => {
      showAdminDropdown.value = !showAdminDropdown.value;
      showUserDropdown.value = false;
    };

    const toggleUserDropdown = () => {
      showUserDropdown.value = !showUserDropdown.value;
      showAdminDropdown.value = false;
    };

    const logout = () => {
      localStorage.clear();
      updateAuthState();
      router.push("/");
    };

    return {
      isAdmin,
      isLoggedIn,
      userName,
      showAdminDropdown,
      showUserDropdown,
      toggleAdminDropdown,
      toggleUserDropdown,
      logout,
    };
  },
};
</script>
