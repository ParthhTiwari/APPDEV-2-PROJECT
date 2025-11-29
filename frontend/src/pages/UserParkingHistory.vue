<template>
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
  max-width: 900px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

.page-title {
  font-size: 28px;
  margin-bottom: 20px;
  color: #222;
  font-weight: bold;
}

.loader {
  font-size: 18px;
  text-align: center;
  padding: 20px;
}

.no-history {
  background: #f3f3f3;
  padding: 15px;
  border-left: 4px solid #666;
  border-radius: 4px;
  font-size: 16px;
  color: #444;
}

.history-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.history-table th,
.history-table td {
  border: 1px solid #ddd;
  padding: 10px 12px;
  text-align: left;
}

.history-table th {
  background: #fafafa;
  font-weight: bold;
  color: #333;
}

.history-table tr:nth-child(even) {
  background: #fcfcfc;
}

.back-btn {
  display: inline-block;
  margin-top: 25px;
  padding: 10px 18px;
  background: #000;
  color: #fff;
  border-radius: 4px;
  text-decoration: none;
  font-size: 15px;
  transition: 0.25s ease;
}

.back-btn:hover {
  opacity: 0.8;
}
</style>
