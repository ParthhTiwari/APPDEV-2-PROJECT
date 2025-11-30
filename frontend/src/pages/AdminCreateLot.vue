<template>
  <div class="dashboard-bg">
    <div
      style="
        min-height:100vh;
        display:flex;
        align-items:center;
        justify-content:center;
        padding:20px;
        box-sizing:border-box;
      "
    >
      <div style="width:100%; max-width:520px; padding:20px">
        <div class="card-box">

          <h2 class="title">
            <span style="font-size:1.9rem">➕</span>
            Create Parking Lot
          </h2>

          <form @submit.prevent="createLot">

            <div class="form-group">
              <label class="label">Lot Name</label>
              <input
                v-model="form.name"
                type="text"
                placeholder="e.g., Downtown Parking"
                required
                class="input-field"
              />
            </div>

            <div class="form-group">
              <label class="label">Location</label>
              <input
                v-model="form.location"
                type="text"
                placeholder="e.g., Main Street, City"
                required
                class="input-field"
              />
            </div>

            <div class="form-group">
              <label class="label">Price per Hour (₹)</label>
              <input
                v-model.number="form.price"
                type="number"
                placeholder="e.g., 50"
                step="0.01"
                required
                class="input-field"
              />
            </div>

            <div class="form-group">
              <label class="label">Number of Spots</label>
              <input
                v-model.number="form.max_spots"
                type="number"
                min="1"
                placeholder="e.g., 100"
                required
                class="input-field"
              />
            </div>

            <button
              type="submit"
              :disabled="loading"
              class="submit-btn"
            >
              {{ loading ? 'Creating...' : 'Create Lot' }}
            </button>
          </form>

          <div v-if="error" class="error-box">
            {{ error }}
          </div>

          <div v-if="success" class="success-box">
            {{ success }}
          </div>
        </div>

        <router-link to="/admin/dashboard" class="back-btn">
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
/* ----------------------------- */
/* MAIN BACKGROUND */
.dashboard-bg {
  min-height: 100vh;
  padding: 40px 0;
  background: #000;
}

/* ----------------------------- */
/* CARD STYLING */
.card-box {
  background: #111;            /* soft black */
  border-radius: 18px;
  padding: 24px 26px 26px;
  border: 1px solid #fff;
  color: white;
}

/* Title white */
.title {
  margin-bottom: 20px;
  font-size: 1.6rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
}

/* Label should always be white */
.label {
  display: block;
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 6px;
  color: white;
}

/* INPUT STYLING */
.input-field {
  width: 100%;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid white;
  font-size: 1rem;
  outline: none;
  background: black;
  color: white;
  transition: 0.25s ease;
}

.input-field:focus {
  border-color: #ccc;
}

/* ----------------------------- */
/* SUBMIT BUTTON (white ↔ black invert) */
.submit-btn {
  width: 100%;
  padding: 12px 0;
  border-radius: 10px;
  background: white;
  color: black;
  border: 1px solid white;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: 0.3s ease;
}

.submit-btn:hover {
  background: black;
  color: white;
  border: 1px solid white;
}

/* ----------------------------- */
/* ERROR BOX */
.error-box {
  margin-top: 14px;
  padding: 10px 12px;
  border-radius: 8px;
  background: #ffebeb;
  color: #b10000;
  border: 1px solid #b10000;
}

/* SUCCESS BOX */
.success-box {
  margin-top: 14px;
  padding: 10px 12px;
  border-radius: 8px;
  background: #0f0f0f;
  color: white;
  border: 1px solid white;
}

/* ----------------------------- */
/* BACK BUTTON */
.back-btn {
  display: inline-block;
  margin-top: 24px;
  color: white;
  text-decoration: none;
  padding: 8px 14px;
  border-radius: 8px;
  background: black;
  border: 1px solid white;
  transition: 0.25s ease;
}

.back-btn:hover {
  background: white;
  color: black;
}
</style>
