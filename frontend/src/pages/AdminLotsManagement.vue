<template>
  <div class="dashboard-bg">
    <div
      style="
        max-width:1200px;
        margin:40px auto 30px;
        display:flex;
        gap:24px;
        align-items:flex-start;
      "
    >
      <!-- Left: List of lots -->
      <div style="flex:2;">
        <h1
          style="
            font-size:2rem;
            font-weight:700;
            margin-bottom:24px;
            display:flex;
            align-items:center;
            gap:8px;
          "
        >
          <span style="font-size:2.2rem;"></span>
          <span style="color:white;">Manage Parking Lots</span>
        </h1>

        <div v-if="loading" style="text-align:center; padding:40px 0;">
          Loading...
        </div>

        <div v-else>
          <div
            v-if="lots.length"
            style="display:flex; flex-wrap:wrap; gap:22px;"
          >
            <div
              v-for="lot in lots"
              :key="lot.lot_id"
              style="
                background:white;
                width:260px;
                border-radius:16px;
                border:1px solid white;
                overflow:hidden;
              "
            >
              <div
                style="
                  background:black;
                  color:white;
                  padding:14px 16px;
                "
              >
                <h5
                  style="
                    margin:0;
                    font-size:1.1rem;
                    font-weight:600;
                  "
                >
                  {{ lot.name }}
                </h5>
              </div>

              <div
                style="
                  padding:14px 16px;
                  font-size:0.97rem;
                  color:#111827;
                "
              >
                <p><strong>Location:</strong> {{ lot.location }}</p>
                <p><strong>Price/Hour:</strong> ₹{{ lot.price }}</p>
                <p><strong>Total Spots:</strong> {{ lot.total_spots }}</p>

                <p>
                  <strong>Available:</strong>
                  <span
                    style="
                      background:black;
                      color:white;
                      border-radius:999px;
                      padding:3px 10px;
                    "
                  >
                    {{ lot.available_spots }}
                  </span>
                </p>

                <p>
                  <strong>Occupied:</strong>
                  <span
                    style="
                      background:black;
                      color:white;
                      border-radius:999px;
                      padding:3px 10px;
                    "
                  >
                    {{ lot.total_spots - lot.available_spots }}
                  </span>
                </p>
              </div>

              <div
                style="
                  padding:10px 16px;
                  border-top:1px solid #e5e7eb;
                  display:flex;
                  justify-content:flex-end;
                  gap:8px;
                "
              >
                <button
                  @click="startEdit(lot)"
                  style="
                    background:black;
                    color:white;
                    border:none;
                    padding:6px 14px;
                    border-radius:6px;
                    font-size:0.9rem;
                    cursor:pointer;
                  "
                >
                  ✏️ Edit
                </button>

                <button
                  @click="deleteLot(lot.lot_id)"
                  style="
                    background:black;
                    color:white;
                    border:none;
                    padding:6px 14px;
                    border-radius:6px;
                    font-size:0.9rem;
                    cursor:pointer;
                  "
                >
                  🗑️ Delete
                </button>
              </div>
            </div>
          </div>

          <div
            v-else
            style="
              text-align:center;
              padding:40px 0;
              color:#4b5563;
            "
          >
            No parking lots found.
          </div>
        </div>

        <router-link
          to="/admin/dashboard"
          style="
            display:inline-block;
            margin-top:24px;
            color:#374151;
            text-decoration:none;
            border:1px solid white;
            padding:8px 14px;
            border-radius:8px;
            background:rgba(255,255,255,0.7);
          "
        >
          ← Back to Dashboard
        </router-link>
      </div>

      <!-- Right: Edit form -->
      <div v-if="selectedLot" style="flex:1.3;">
        <div
          style="
            background:white;
            border-radius:16px;
            box-shadow:0 2px 12px rgba(0,0,0,0.12);
            padding:18px 20px;
          "
        >
          <h3
            style="
              margin-bottom:14px;
              font-size:1.25rem;
              font-weight:600;
            "
          >
            ✏️ Edit Lot #{{ editForm.lot_id }}
          </h3>

          <form @submit.prevent="saveEdit">
            <div style="margin-bottom:10px;">
              <label>Lot Name</label>
              <input
                v-model="editForm.name"
                type="text"
                required
                style="
                  width:100%;
                  padding:8px;
                  border-radius:8px;
                  border:1px solid #d1d5db;
                "
              />
            </div>

            <div style="margin-bottom:10px;">
              <label>Location</label>
              <input
                v-model="editForm.location"
                type="text"
                required
                style="
                  width:100%;
                  padding:8px;
                  border-radius:8px;
                  border:1px solid #d1d5db;
                "
              />
            </div>

            <div style="margin-bottom:10px;">
              <label>Price/Hour (₹)</label>
              <input
                v-model.number="editForm.price"
                type="number"
                step="0.01"
                required
                style="
                  width:100%;
                  padding:8px;
                  border-radius:8px;
                  border:1px solid #d1d5db;
                "
              />
            </div>

            <div style="margin-bottom:14px;">
              <label>Total Spots</label>
              <input
                v-model.number="editForm.total_spots"
                type="number"
                min="0"
                required
                style="
                  width:100%;
                  padding:8px;
                  border-radius:8px;
                  border:1px solid #d1d5db;
                "
              />
              <div
                style="
                  font-size:0.8rem;
                  color:#6b7280;
                  margin-top:3px;
                "
              >
                (0 karoge toh lot delete ho sakta hai, backend logic ke
                hisaab se)
              </div>
            </div>

            <button
              type="submit"
              :disabled="saving"
              style="
                width:100%;
                padding:9px 0;
                border:none;
                border-radius:10px;
                background:#16a34a;
                color:white;
                font-weight:600;
                font-size:0.95rem;
                cursor:pointer;
              "
            >
              {{ saving ? "Saving..." : "Save Changes" }}
            </button>

            <button
              type="button"
              @click="cancelEdit"
              style="
                width:100%;
                margin-top:8px;
                padding:8px 0;
                border:none;
                border-radius:10px;
                background:#e5e7eb;
                color:#374151;
                font-weight:500;
                font-size:0.9rem;
                cursor:pointer;
              "
            >
              Cancel
            </button>
          </form>

          <div
            v-if="editError"
            style="
              margin-top:10px;
              padding:8px 10px;
              border-radius:8px;
              background:#fee2e2;
              color:#b91c1c;
              font-size:0.85rem;
            "
          >
            {{ editError }}
          </div>

          <div
            v-if="editSuccess"
            style="
              margin-top:10px;
              padding:8px 10px;
              border-radius:8px;
              background:#dcfce7;
              color:#166534;
              font-size:0.85rem;
            "
          >
            {{ editSuccess }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { adminAPI } from "../services/api";

export default {
  setup() {
    const loading = ref(true);
    const lots = ref([]);

    const adminEmail = localStorage.getItem("admin_email");
    const adminPassword = localStorage.getItem("admin_password");

    const selectedLot = ref(null);
    const editForm = ref({
      lot_id: null,
      name: "",
      location: "",
      price: "",
      total_spots: 0,
    });

    const saving = ref(false);
    const editError = ref("");
    const editSuccess = ref("");

    onMounted(async () => {
      try {
        const res = await adminAPI.getLots(adminEmail, adminPassword);
        lots.value = res.data.lots || [];
      } catch (err) {
        console.error("Failed to load lots", err);
      } finally {
        loading.value = false;
      }
    });

    const startEdit = (lot) => {
      selectedLot.value = lot;
      editForm.value = {
        lot_id: lot.lot_id,
        name: lot.name,
        location: lot.location,
        price: lot.price,
        total_spots: lot.total_spots,
      };
      editError.value = "";
      editSuccess.value = "";
    };

    const cancelEdit = () => {
      selectedLot.value = null;
    };

    const saveEdit = async () => {
      saving.value = true;
      editError.value = "";
      editSuccess.value = "";

      try {
        await adminAPI.updateLot(
          editForm.value.lot_id,
          {
            name: editForm.value.name,
            location: editForm.value.location,
            price: editForm.value.price,
            max_spots: editForm.value.total_spots,
          },
          adminEmail,
          adminPassword
        );

        const idx = lots.value.findIndex(
          (l) => l.lot_id === editForm.value.lot_id
        );
        if (idx !== -1) {
          lots.value[idx].name = editForm.value.name;
          lots.value[idx].location = editForm.value.location;
          lots.value[idx].price = editForm.value.price;
          lots.value[idx].total_spots = editForm.value.total_spots;
        }

        editSuccess.value = "Lot updated successfully";
        setTimeout(() => {
          selectedLot.value = null;
        }, 1000);
      } catch (err) {
        editError.value =
          err.response?.data?.error || "Failed to update lot";
      } finally {
        saving.value = false;
      }
    };

    const deleteLot = async (lotId) => {
      if (!confirm("Are you sure? This lot will be deleted.")) return;
      try {
        await adminAPI.deleteLot(lotId, adminEmail, adminPassword);
        lots.value = lots.value.filter((l) => l.lot_id !== lotId);
      } catch (err) {
        alert(
          "Failed to delete: " +
            (err.response?.data?.error || "Unknown error")
        );
      }
    };

    return {
      loading,
      lots,
      selectedLot,
      editForm,
      saving,
      editError,
      editSuccess,
      startEdit,
      cancelEdit,
      saveEdit,
      deleteLot,
    };
  },
};
</script>

<style scoped>
.dashboard-bg {
  min-height: 100vh;
  padding: 40px 0;
  background: url("/images/admin-dashboard.jpg") center/cover fixed;
  backdrop-filter: blur(3px);
}
</style>
  