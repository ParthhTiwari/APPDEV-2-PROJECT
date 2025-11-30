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
  background: black;        /* FULL BLACK BACKGROUND */
}

.report-card {
  width: 100%;
  max-width: 850px;
  background: #0e0e0e;      /* PURE DARK CARD */
  border: 1px solid white;  /* WHITE BORDER */
  border-radius: 16px;
  padding: 28px;
  color: white;             /* WHITE TEXT */
}

.report-card h2 {
  font-size: 26px;
  margin-bottom: 10px;
  color: white;
  border-bottom: 1px solid white;
  padding-bottom: 8px;
}

.month-label {
  font-size: 18px;
  margin-bottom: 20px;
  color: #ccc;
}

/* ===== Stats Section ===== */
.stats-grid {
  display: flex;
  gap: 16px;
  margin-bottom: 28px;
}

.stat-card {
  flex: 1;
  border: 1px solid white;
  padding: 18px;
  border-radius: 12px;
  background: transparent;
  color: white;
  text-align: center;
  transition: 0.3s;
}

.stat-card:hover {
  background: rgba(255, 255, 255, 0.1);
}

.stat-card h3 {
  margin: 0 0 8px;
  font-size: 22px;
}

/* ===== Table ===== */
.table-title {
  margin: 18px 0 8px;
  font-size: 20px;
  color: white;
  border-bottom: 1px solid white;
  padding-bottom: 6px;
}

.activity-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 16px;
}

.activity-table th,
.activity-table td {
  border: 1px solid white;
  padding: 10px 12px;
  font-size: 14px;
  color: white;
}

.activity-table th {
  background: rgba(255, 255, 255, 0.1);
}

/* ===== Empty text ===== */
.empty-text {
  color: #bbb;
  margin: 16px 0;
  font-style: italic;
}

/* ===== Back Button ===== */
.back-link {
  display: inline-block;
  margin-top: 14px;
  text-decoration: none;
  color: white;
  border: 1px solid white;
  padding: 8px 14px;
  border-radius: 8px;
  transition: 0.3s;
}

.back-link:hover {
  background: white;
  color: black;
}

/* ===== Error ===== */
.error {
  color: #ff5d5d;
  margin-top: 8px;
}
</style>
