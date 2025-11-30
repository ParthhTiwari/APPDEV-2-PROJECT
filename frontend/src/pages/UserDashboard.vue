<template>
  <div class="dashboard-bg">
    <h1 class="title">Your Dashboard</h1>

    <h2 class="section-title">Your Active Parked Vehicles</h2>

    <div v-if="activeParkings.length === 0" class="empty-box">
      No active parked vehicles.
    </div>

    <div class="list-container">
      <div
        v-for="vehicle in activeParkings"
        :key="vehicle.vehicle_id"
        class="card active-card"
      >
        <h3>🚗 {{ vehicle.number_plate }}</h3>
        <p><strong>Lot:</strong> {{ vehicle.lot_name }}</p>
        <p><strong>Spot:</strong> #{{ vehicle.spot_number }}</p>
        <p><strong>Parked Since:</strong> {{ vehicle.entry_time }}</p>

        <button
          @click="unparkVehicle(vehicle.vehicle_id)"
          class="btn warning"
        >
          🚪 Unpark Vehicle
        </button>
      </div>
    </div>

    <div class="feature-card reminders-card">
      <div class="card-icon">🔔</div>
      <div class="card-content">
        <h4>Daily Reminders</h4>
        <p>Automated emails for inactive users (3+ days)</p>
        <div class="status-badge success">
          ✅ Celery Beat: Every 24h
        </div>
        <small>Next: {{ nextReminder() }}</small>
      </div>
    </div>

    <h2 class="section-title">Available Parking Lots</h2>

    <div v-if="loading" class="loading">Loading...</div>

    <div class="list-container" v-else>
      <div v-for="lot in lots" :key="lot.lot_id" class="card">
        <h3>{{ lot.name }}</h3>
        <p><strong>📍 Location:</strong> {{ lot.location }}</p>
        <p><strong>💰 Price:</strong> ₹{{ lot.price }}/hour</p>
        <p>
          <strong>Available Spots:</strong>
          <span class="tag green">
            {{ lot.available_spots }} / {{ lot.total_spots }}
          </span>
        </p>
        <button
          @click="parkVehicle(lot.lot_id)"
          class="btn primary"
        >
          Park Here
        </button>
      </div>
    </div>

    <div class="actions">
      <router-link to="/user/history" class="btn info">
        📜 History
      </router-link>

      <router-link to="/user/export" class="btn secondary">
        📥 Export
      </router-link>

      <router-link to="/user/monthly-report" class="btn secondary">
        📊 Monthly Report
      </router-link>
    </div>

    <div v-if="showParkModal" class="modal-overlay">
      <div class="modal-box">
        <div class="modal-header">
          <h3>Park Your Vehicle</h3>
          <button
            @click="showParkModal = false"
            class="close-btn"
          >
            ✖
          </button>
        </div>

        <div class="modal-body">
          <label>Vehicle Number Plate</label>
          <input
            v-model="vehicleNumber"
            type="text"
            class="modal-input"
            placeholder="e.g., MH12AB1234"
          />
        </div>

        <div class="modal-footer">
          <button
            @click="showParkModal = false"
            class="btn secondary"
          >
            Cancel
          </button>
          <button @click="confirmPark" class="btn primary">
            {{ parkingLoading ? "Parking..." : "Confirm Park" }}
          </button>
        </div>
      </div>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { userAPI } from "../services/api";

export default {
  setup() {
    const loading = ref(true);
    const parkingLoading = ref(false);
    const error = ref("");
    const lots = ref([]);
    const activeParkings = ref([]);
    const showParkModal = ref(false);
    const vehicleNumber = ref("");
    const selectedLotId = ref(null);

    const userId = localStorage.getItem("user_id");

    const nextReminder = () => {
      const now = new Date();
      const next = new Date(now.getTime() + 24 * 60 * 60 * 1000);
      return next.toLocaleDateString();
    };

    const refreshDashboard = async () => {
      try {
        const response = await userAPI.dashboard(userId);
        lots.value = response.data.parking_lots || [];
        activeParkings.value = response.data.active_parkings || [];
      } catch {
        error.value = "Failed to load dashboard";
      } finally {
        loading.value = false;
      }
    };

    onMounted(refreshDashboard);

    const parkVehicle = (lotId) => {
      selectedLotId.value = lotId;
      showParkModal.value = true;
    };

    const confirmPark = async () => {
      if (!vehicleNumber.value) {
        error.value = "Please enter vehicle number";
        return;
      }

      parkingLoading.value = true;

      try {
        await userAPI.parkVehicle({
          user_id: userId,
          vehicle_number: vehicleNumber.value,
          lot_id: selectedLotId.value,
        });

        showParkModal.value = false;
        vehicleNumber.value = "";
        await refreshDashboard();
      } catch (err) {
        error.value =
          err.response?.data?.error || "Failed to park vehicle";
      } finally {
        parkingLoading.value = false;
      }
    };

    const unparkVehicle = async (vehicleId) => {
      try {
        const response = await userAPI.unparkVehicle(vehicleId);
        await refreshDashboard();
        alert(`Unparked! Cost: ₹${response.data.cost}`);
      } catch (err) {
        error.value =
          err.response?.data?.error || "Failed to unpark";
      }
    };

    return {
      loading,
      parkingLoading,
      error,
      lots,
      activeParkings,
      showParkModal,
      vehicleNumber,
      selectedLotId,
      parkVehicle,
      confirmPark,
      unparkVehicle,
      nextReminder,
    };
  },
};
</script>

<style scoped>
/* ===========================
   MAIN BACKGROUND
   =========================== */
.dashboard-bg {
  min-height: 100vh;
  width: 100%;
  background: black;
  overflow-y: auto;
  padding: 25px;
  box-sizing: border-box;
  color: white;
  border: 1px solid white;
}

/* ===========================
   TITLES
   =========================== */
.title {
  font-size: 28px;
  font-weight: 700;
  color: white;
  padding: 10px 14px;
  border: 1px solid white;
  border-radius: 10px;
  background: black;
  width: fit-content;
}

.section-title {
  font-size: 22px;
  margin-top: 25px;
  padding: 10px 14px;
  border: 1px solid white;
  border-radius: 10px;
  background: black;
  color: white;
  width: fit-content;
}

/* ===========================
   LIST / CARDS
   =========================== */
.list-container {
  display: flex;
  flex-direction: column;
  gap: 18px;
  margin-top: 18px;
}

.card {
  background: rgba(255, 255, 255, 0.05); /* light transparent white */
  border: 1px solid white;
  border-radius: 12px;
  padding: 18px;
  color: white;
}

.active-card {
  border-left: 6px solid white; /* Premium left highlight */
}

.empty-box {
  background: rgba(255, 255, 255, 0.08);
  padding: 18px;
  border-radius: 10px;
  text-align: center;
  font-weight: 600;
  color: white;
  border: 1px solid white;
}

/* ===========================
   BUTTONS
   =========================== */
.btn {
  padding: 10px 15px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 10px;
  display: inline-block;
  text-decoration: none;
  border: 1px solid white;
  transition: 0.3s ease;
}

.btn.primary,
.btn.warning,
.btn.secondary,
.btn.info {
  background: transparent;
  color: white;
}

.btn:hover {
  background: white;
  color: black;
}

/* ===========================
   ACTION BUTTONS GROUP
   =========================== */
.actions {
  position: absolute;
  top: 80px;
  right: 25px;
  display: flex;
  gap: 10px;
  border: 1px solid white;
  border-radius: 40px;
  padding: 8px 14px;
  background: black;
}

/* ===========================
   MODAL
   =========================== */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-box {
  background: black;
  width: 330px;
  padding: 22px;
  border-radius: 12px;
  border: 1px solid white;
  color: white;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-btn {
  background: transparent;
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
}

.modal-input {
  width: 100%;
  padding: 10px;
  background: transparent;
  border: 1px solid white;
  color: white;
  border-radius: 8px;
  margin-top: 8px;
}

/* ===========================
   FEATURE CARD (Reminders)
   =========================== */
.feature-card {
  display: flex;
  gap: 15px;
  padding: 20px;
  border-radius: 12px;
  margin: 25px 0;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid white;
  color: white;
}

.card-icon {
  font-size: 30px;
}

.card-content h4 {
  margin: 0;
  font-size: 18px;
  color: white;
}

.card-content p {
  margin: 6px 0;
  color: white;
}

.status-badge {
  background: transparent;
  border: 1px solid white;
  color: white;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 12px;
  display: inline-block;
  margin-top: 6px;
}

.tag.green {
  background: transparent;
  border: 1px solid white;
  color: white;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 14px;
}

/* ===========================
   ERROR TEXT
   =========================== */
.error {
  color: red;
  margin-top: 10px;
  font-weight: 600;
}
</style>
