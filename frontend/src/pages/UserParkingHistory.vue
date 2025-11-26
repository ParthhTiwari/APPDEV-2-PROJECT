<!-- filepath: frontend/src/pages/UserParkingHistory.vue -->
<template>
  <div class="container mt-5">
    <h1 class="mb-4">📜 Your Parking History</h1>

    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else>
      <div v-if="history.length === 0" class="alert alert-info">
        You don't have any parking history yet.
      </div>

      <table v-else class="table table-striped">
        <thead>
          <tr>
            <th>Vehicle</th>
            <th>Lot</th>
            <th>Spot</th>
            <th>Entry Time</th>
            <th>Exit Time</th>
            <th>Duration</th>
            <th>Cost</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in history" :key="record.vehicle_id">
            <td>{{ record.number_plate }}</td>
            <td>{{ record.lot_name }}</td>
            <td>#{{ record.spot_number }}</td>
            <td>{{ record.entry_time }}</td>
            <td>{{ record.exit_time || 'Still parked' }}</td>
            <td>{{ record.hours || 'N/A' }}</td>
            <td>₹{{ record.cost || record.provisional_cost || 0 }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <router-link to="/user/dashboard" class="btn btn-secondary mt-4">
      ← Back to Dashboard
    </router-link>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { userAPI } from '../services/api';

export default {
  setup() {
    const loading = ref(true);
    const history = ref([]);
    const userId = localStorage.getItem('user_id');

    onMounted(async () => {
      try {
        const response = await userAPI.history(userId);
        history.value = response.data.history || [];
      } catch (err) {
        console.error('Failed to load history:', err);
      } finally {
        loading.value = false;
      }
    });

    return {
      loading,
      history
    };
  }
};
</script>