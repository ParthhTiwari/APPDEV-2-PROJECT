<template>
  <div class="dashboard-bg">
    <div
      style="
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
        box-sizing: border-box;
      "
    >
      <div style="width: 100%; max-width: 520px; padding: 20px">
        <div
          style="background: grey; border-radius: 18px; padding: 24px 26px 26px"
        >
          <h2
            style="
              margin-bottom: 20px;
              font-size: 1.6rem;
              font-weight: 700;
              display: flex;
              align-items: center;
              gap: 8px;
              color: #111827;
            "
          >
            <span style="font-size: 1.9rem">➕</span>
            Create Parking Lot
          </h2>

          <form @submit.prevent="createLot">
            <div style="margin-bottom: 14px">
              <label
                style="
                  display: block;
                  font-size: 0.95rem;
                  font-weight: 600;
                  margin-bottom: 6px;
                  color: #374151;
                "
              >
                Lot Name
              </label>
              <input
                v-model="form.name"
                type="text"
                placeholder="e.g., Downtown Parking"
                required
                style="
                  width: 100%;
                  padding: 9px 11px;
                  border-radius: 8px;
                  border: 1px solid #d1d5db;
                  font-size: 0.98rem;
                  outline: none;
                "
              />
            </div>

            <div style="margin-bottom: 14px">
              <label
                style="
                  display: block;
                  font-size: 0.95rem;
                  font-weight: 600;
                  margin-bottom: 6px;
                  color: #374151;
                "
              >
                Location
              </label>
              <input
                v-model="form.location"
                type="text"
                placeholder="e.g., Main Street, City"
                required
                style="
                  width: 100%;
                  padding: 9px 11px;
                  border-radius: 8px;
                  border: 1px solid #d1d5db;
                  font-size: 0.98rem;
                  outline: none;
                "
              />
            </div>

            <div style="margin-bottom: 14px">
              <label
                style="
                  display: block;
                  font-size: 0.95rem;
                  font-weight: 600;
                  margin-bottom: 6px;
                  color: #374151;
                "
              >
                Price per Hour (₹)
              </label>
              <input
                v-model.number="form.price"
                type="number"
                placeholder="e.g., 50"
                step="0.01"
                required
                style="
                  width: 100%;
                  padding: 9px 11px;
                  border-radius: 8px;
                  border: 1px solid #d1d5db;
                  font-size: 0.98rem;
                  outline: none;
                "
              />
            </div>

            <div style="margin-bottom: 18px">
              <label
                style="
                  display: block;
                  font-size: 0.95rem;
                  font-weight: 600;
                  margin-bottom: 6px;
                  color: #374151;
                "
              >
                Number of Spots
              </label>
              <input
                v-model.number="form.max_spots"
                type="number"
                min="1"
                placeholder="e.g., 100"
                required
                style="
                  width: 100%;
                  padding: 9px 11px;
                  border-radius: 8px;
                  border: 1px solid #d1d5db;
                  font-size: 0.98rem;
                  outline: none;
                "
              />
            </div>

            <button
              type="submit"
              :disabled="loading"
              style="
                width: 100%;
                padding: 10px 0;
                border: none;
                border-radius: 10px;
                background: black;
                color: white;
                font-weight: 600;
                font-size: 1rem;
                cursor: pointer;
              "
            >
              {{ loading ? "Creating..." : "Create Lot" }}
            </button>
          </form>

          <div
            v-if="error"
            style="
              margin-top: 14px;
              padding: 10px 12px;
              border-radius: 8px;
              background: #fee2e2;
              color: #b91c1c;
              font-size: 0.95rem;
            "
          >
            {{ error }}
          </div>

          <div
            v-if="success"
            style="
              margin-top: 14px;
              padding: 10px 12px;
              border-radius: 8px;
              background: #dcfce7;
              color: #166534;
              font-size: 0.95rem;
            "
          >
            {{ success }}
          </div>
        </div>

        <router-link
          to="/admin/dashboard"
          style="
            display: inline-block;
            margin-top: 24px;
            color: #374151;
            text-decoration: none;
            border: 1px solid white;
            padding: 8px 14px;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.7);
          "
        >
          ← Back to Dashboard
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { adminAPI } from "../services/api";

export default {
  setup() {
    const router = useRouter();
    const loading = ref(false);
    const error = ref("");
    const success = ref("");

    const form = ref({
      name: "",
      location: "",
      price: "",
      max_spots: "",
    });

    const adminEmail = localStorage.getItem("admin_email");
    const adminPassword = localStorage.getItem("admin_password");

    const createLot = async () => {
      loading.value = true;
      error.value = "";
      success.value = "";

      try {
        const response = await adminAPI.createLot(
          form.value,
          adminEmail,
          adminPassword
        );

        success.value = response.data.message || "Lot created successfully!";

        form.value = {
          name: "",
          location: "",
          price: "",
          max_spots: "",
        };

        setTimeout(() => {
          router.push("/admin/dashboard");
        }, 1200);
      } catch (err) {
        error.value = err.response?.data?.error || "Failed to create lot";
      } finally {
        loading.value = false;
      }
    };

    return {
      form,
      loading,
      error,
      success,
      createLot,
    };
  },
};
</script>

<style scoped>
.dashboard-bg {
  min-height: 100vh;
  padding: 40px 0;
  background: url("/images/admin-dashboard.jpg") center/cover no-repeat fixed;
  backdrop-filter: blur(3px);
}
</style>
