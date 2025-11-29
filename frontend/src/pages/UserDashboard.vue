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
.dashboard-bg {
  min-height: 100vh;
  width: 100%;
  background: black;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  overflow-y: hidden;
  padding: 20px;
  box-sizing: border-box;
}

.title {
  font-size: 26px;
  font-weight: 700;
  color: white;
  text-shadow: 1px 1px 3px black;
  width: fit-content;
  padding: 7px 10px;
  border: 1px solid white;
  border-radius: 8px;
  background: black;
}

.section-title {
  font-size: 20px;
  margin-top: 25px;
  width: fit-content;
  padding: 10px 14px;
  color: white;
  border: 1px solid white;
  border-radius: 8px;
  background: black;
}

.list-container {
  display: flex;
  flex-direction: column;
  gap: 18px;
  margin-top: 15px;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 18px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15);
}

.active-card {
  background: rgba(255, 240, 180, 0.9);
  border-left: 6px solid #ffb100;
}

.empty-box {
  background: rgba(255, 255, 255, 0.8);
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  font-weight: 600;
}

.btn {
  padding: 9px 14px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 10px;
  display: inline-block;
  text-decoration: none;
}

.btn.primary {
  background: black;
  color: white;
}
.btn.warning {
  background: #ff9800;
  color: white;
}
.btn.secondary {
  background: black;
  color: white;
}
.btn.info {
  background: black;
  color: white;
}

.actions {
  position: absolute;
  top: 80px;
  right: 25px;
  display: flex;
  gap: 8px;
  border: 1px solid white;
  border-radius: 40px;
  padding: 8px 12px;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-box {
  background: white;
  width: 320px;
  padding: 20px;
  border-radius: 12px;
}

.error {
  color: red;
  margin-top: 10px;
  font-weight: 600;
}

.feature-card {
  display: flex;
  gap: 15px;
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 12px;
  margin: 25px 0;
  background: rgba(255, 255, 255, 0.95);
}

.card-icon {
  font-size: 28px;
}

.card-content h4 {
  margin: 0 0 8px 0;
  color: #333;
}

.card-content p {
  margin: 5px 0;
  color: #666;
}

.status-badge {
  background: #28a745;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  display: inline-block;
  margin-top: 8px;
}

.tag.green {
  background: #28a745;
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 14px;
}
</style>
