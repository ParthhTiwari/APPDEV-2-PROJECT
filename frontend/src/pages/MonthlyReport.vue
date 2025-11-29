<template>
  <div class="report-container">
    <div class="report-card">
      <h2>📊 Monthly Parking Report</h2>
      <p class="month-label">{{ month }}</p>

      <div class="stats-grid">
        <div class="stat-card">
          <h3>{{ totalSessions }}</h3>
          <p>Total Sessions</p>
        </div>
        <div class="stat-card">
          <h3>₹{{ totalAmount }}</h3>
          <p>Total Amount</p>
        </div>
        <div class="stat-card">
          <h3>{{ mostUsedLot }}</h3>
          <p>Most Used Lot</p>
        </div>
      </div>

      <h3 class="table-title">Recent Activity</h3>
      <table class="activity-table" v-if="recentActivity.length">
        <thead>
          <tr>
            <th>Vehicle</th>
            <th>Lot</th>
            <th>Entry Time</th>
            <th>Exit Time</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in recentActivity" :key="row.id">
            <td>{{ row.number_plate }}</td>
            <td>{{ row.lot_name }}</td>
            <td>{{ row.entry_time }}</td>
            <td>{{ row.exit_time }}</td>
          </tr>
        </tbody>
      </table>

      <p v-else class="empty-text">
        No parking activity recorded for this month.
      </p>

      <router-link to="/user/dashboard" class="back-link">
        ← Back to Dashboard
      </router-link>

      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { userAPI } from "../services/api";

export default {
  setup() {
    const month = ref("");
    const totalSessions = ref(0);
    const totalAmount = ref(0);
    const mostUsedLot = ref("N/A");
    const recentActivity = ref([]);
    const error = ref("");
    const userId = localStorage.getItem("user_id");

    const loadSummary = async () => {
      try {
        const response = await userAPI.monthlySummary(userId);
        month.value = response.data.month;
        totalSessions.value = response.data.total_sessions;
        totalAmount.value = response.data.total_amount;
        mostUsedLot.value = response.data.most_used_lot;
        recentActivity.value = response.data.recent_activity || [];
      } catch {
        error.value = "Failed to load monthly report";
      }
    };

    onMounted(loadSummary);

    return {
      month,
      totalSessions,
      totalAmount,
      mostUsedLot,
      recentActivity,
      error,
    };
  },
};
</script>

<style scoped>
.report-container {
  min-height: 100vh;
  padding: 30px;
  display: flex;
  justify-content: center;
  background: #f3f4f6;
}

.report-card {
  width: 100%;
  max-width: 800px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  padding: 24px 28px;
}

.report-card h2 {
  margin: 0 0 8px 0;
}

.month-label {
  margin: 0 0 20px 0;
  color: #666;
}

.stats-grid {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  flex: 1;
  padding: 16px;
  border-radius: 12px;
  background: #f9fafb;
  text-align: center;
}

.stat-card h3 {
  margin: 0 0 6px 0;
}

.table-title {
  margin: 10px 0;
}

.activity-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 16px;
}

.activity-table th,
.activity-table td {
  border: 1px solid #ddd;
  padding: 8px 10px;
  font-size: 14px;
}

.activity-table th {
  background: #f1f1f1;
}

.empty-text {
  color: #666;
  margin: 16px 0;
}

.back-link {
  display: inline-block;
  margin-top: 10px;
  text-decoration: none;
  color: #111;
  border: 1px solid #111;
  padding: 6px 12px;
  border-radius: 8px;
}

.error {
  color: red;
  margin-top: 8px;
}
</style>
