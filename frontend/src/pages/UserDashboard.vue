<!-- filepath: frontend/src/pages/UserDashboard.vue -->
<template>
  <div class="container mt-5">
    <h1 class="mb-4">🏠 Your Dashboard</h1>

    <!-- Active Parking Section -->
    <div v-if="activeParking" class="alert alert-warning">
      <h5>🚗 Currently Parked</h5>
      <p><strong>Vehicle:</strong> {{ activeParking.number_plate }}</p>
      <p><strong>Lot:</strong> {{ activeParking.lot_name }}</p>
      <p><strong>Spot:</strong> #{{ activeParking.spot_number }}</p>
      <p><strong>Parked Since:</strong> {{ activeParking.entry_time }}</p>
      <button @click="unparkVehicle" class="btn btn-warning">
        🚪 Unpark Vehicle
      </button>
    </div>

    <!-- Available Lots Section -->
    <div class="row">
      <div class="col-md-12 mb-4">
        <h3>🅿️ Available Parking Lots</h3>
      </div>

      <div v-if="loading" class="col-md-12 text-center">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else>
        <div v-for="lot in lots" :key="lot.lot_id" class="col-md-4 mb-4">
          <div class="card shadow">
            <div class="card-body">
              <h5 class="card-title">{{ lot.name }}</h5>
              <p class="card-text">
                <strong>📍 Location:</strong> {{ lot.location }}
              </p>
              <p class="card-text">
                <strong>💰 Price:</strong> ₹{{ lot.price }}/hour
              </p>
              <p class="card-text">
                <strong>Available Spots:</strong>
                <span class="badge bg-success">{{ lot.available_spots }} / {{ lot.total_spots }}</span>
              </p>
              <button 
                @click="parkVehicle(lot.lot_id)" 
                class="btn btn-primary w-100"
                :disabled="!activeParking ? false : true"
              >
                🅿️ Park Here
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="row mt-4">
      <div class="col-md-12">
        <router-link to="/user/history" class="btn btn-info">
          📜 View History
        </router-link>
        <router-link to="/user/export" class="btn btn-secondary ms-2">
          📥 Export Data
        </router-link>
      </div>
    </div>

    <!-- Modal for parking -->
    <div v-if="showParkModal" class="modal d-block" style="background: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Park Your Vehicle</h5>
            <button @click="showParkModal = false" type="button" class="btn-close"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label>Vehicle Number Plate</label>
              <input 
                v-model="vehicleNumber" 
                type="text" 
                class="form-control"
                placeholder="e.g., KA01AB1234"
                required
              >
            </div>
          </div>
          <div class="modal-footer">
            <button @click="showParkModal = false" type="button" class="btn btn-secondary">
              Cancel
            </button>
            <button @click="confirmPark" type="button" class="btn btn-primary" :disabled="parkingLoading">
              {{ parkingLoading ? 'Parking...' : 'Confirm Park' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { userAPI } from '../services/api';

export default {
  setup() {
    const router = useRouter();
    const loading = ref(true);
    const parkingLoading = ref(false);
    const error = ref('');
    const lots = ref([]);
    const activeParking = ref(null);
    const showParkModal = ref(false);
    const vehicleNumber = ref('');
    const selectedLotId = ref(null);

    const userId = localStorage.getItem('user_id');

    onMounted(async () => {
      try {
        const response = await userAPI.dashboard(userId);
        lots.value = response.data.parking_lots || [];
        activeParking.value = response.data.active_parking;
      } catch (err) {
        error.value = 'Failed to load dashboard';
      } finally {
        loading.value = false;
      }
    });

    const parkVehicle = (lotId) => {
      selectedLotId.value = lotId;
      showParkModal.value = true;
    };

    const confirmPark = async () => {
      if (!vehicleNumber.value) {
        error.value = 'Please enter vehicle number';
        return;
      }

      parkingLoading.value = true;
      error.value = '';

      try {
        const response = await userAPI.parkVehicle({
          user_id: userId,
          vehicle_number: vehicleNumber.value,
          lot_id: selectedLotId.value
        });

        showParkModal.value = false;
        vehicleNumber.value = '';
        
        // Reload dashboard
        const dashResponse = await userAPI.dashboard(userId);
        lots.value = dashResponse.data.parking_lots || [];
        activeParking.value = dashResponse.data.active_parking;

      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to park vehicle';
      } finally {
        parkingLoading.value = false;
      }
    };

    const unparkVehicle = async () => {
      if (!activeParking.value) return;

      try {
        const response = await userAPI.unparkVehicle(activeParking.value.vehicle_id);
        
        // Reload dashboard
        const dashResponse = await userAPI.dashboard(userId);
        lots.value = dashResponse.data.parking_lots || [];
        activeParking.value = dashResponse.data.active_parking;

        alert(`Unparked! Cost: ₹${response.data.cost}`);
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to unpark';
      }
    };

    return {
      loading,
      parkingLoading,
      error,
      lots,
      activeParking,
      showParkModal,
      vehicleNumber,
      parkVehicle,
      confirmPark,
      unparkVehicle
    };
  }
};
</script>

<style scoped>
.modal.d-block {
  display: block;
}
</style>