<template>
<div class="bg">
  <div class="history-container">
    <h1 class="page-title">📜 Your Parking History</h1>

    <div v-if="loading" class="loader">Loading...</div>

    <div v-else>
      <div v-if="history.length === 0" class="no-history">
        You don't have any parking history yet.
      </div>

      <table v-else class="history-table">
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
            <td>{{ record.exit_time || "Still parked" }}</td>
            <td>{{ record.hours || "N/A" }}</td>
            <td>₹{{ record.cost || record.provisional_cost || 0 }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <router-link to="/user/dashboard" class="back-btn">
      ← Back to Dashboard
    </router-link>
  </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { userAPI } from "../services/api";

export default {
  setup() {
    const loading = ref(true);
    const history = ref([]);
    const userId = localStorage.getItem("user_id");

    const loadHistory = async () => {
      try {
        const response = await userAPI.history(userId);
        history.value = response.data.history || [];
      } catch (err) {
        console.error("Failed to load history:", err);
      } finally {
        loading.value = false;
      }
    };

    onMounted(loadHistory);

    return {
      loading,
      history,
    };
  },
};
</script>

<style scoped>
.history-container {
  padding: 30px;
  max-width: 950px;
  margin: 0 auto;
  background: black;                      /* Full black background */
  min-height: 100vh;
  color: white;                           /* White text */
  border: 1px solid white;                /* Premium border */
  border-radius: 14px;
}

/* ===== Page Title ===== */
.page-title {
  font-size: 30px;
  margin-bottom: 25px;
  color: white;
  text-align: center;
  border-bottom: 1px solid white;
  padding-bottom: 10px;
}

/* ===== Loader ===== */
.loader {
  font-size: 18px;
  text-align: center;
  padding: 20px;
  color: white;
}

/* ===== No History Message ===== */
.no-history {
  background: rgba(255,255,255,0.1);
  padding: 16px;
  border-left: 4px solid white;
  border-radius: 8px;
  font-size: 17px;
  color: white;
}

/* ===== Table ===== */
.history-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 25px;
  color: white;
  border: 1px solid white;
}

.history-table th,
.history-table td {
  border: 1px solid white;
  padding: 12px 14px;
  text-align: left;
  font-size: 15px;
}

.history-table th {
  background: rgba(255,255,255,0.1);
  font-weight: bold;
  color: white;
}

.history-table tr:nth-child(even) {
  background: rgba(255,255,255,0.05);
}

/* ===== Back Button ===== */
.back-btn {
  display: inline-block;
  margin-top: 30px;
  padding: 12px 18px;
  border: 1px solid white;
  background: transparent;
  color: white;
  border-radius: 8px;
  text-decoration: none;
  font-size: 16px;
  transition: 0.3s ease;
}

.back-btn:hover {
  background: white;
  color: black;
}
.bg{
  background-color: black;
}
</style>
