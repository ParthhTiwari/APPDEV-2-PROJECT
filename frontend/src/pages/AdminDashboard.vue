<template>
  <div class="dashboard-bg">
    <div class="main-container">
      <h1 class="page-title">Admin Dashboard</h1>

      <!-- Stats Cards -->
      <div class="stats-container">
        <div
          v-for="card in statsCards"
          :key="card.label"
          class="stat-card"
        >
          <div class="stat-value">{{ card.value }}</div>
          <div class="stat-label">{{ card.label }}</div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="action-buttons">
        <router-link to="/admin/create-lot" class="btn-white">
          ➕ Create New Lot
        </router-link>

        <router-link to="/admin/lots" class="btn-white">
          🏢 Manage Lots
        </router-link>

        <button @click="showUsers = !showUsers" class="btn-white">
          👥 Show Registered Users
        </button>
      </div>

      <!-- Parking Lots Table -->
      <div class="table-card">
        <div class="card-title">All Parking Lots</div>

        <div v-if="loading" class="loading-box">Loading...</div>

        <table v-else class="main-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Location</th>
              <th>Price/Hour</th>
              <th>Total Spots</th>
              <th>Available</th>
              <th>Occupied</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="lot in lots" :key="lot.lot_id">
              <td>{{ lot.lot_id }}</td>
              <td>{{ lot.name }}</td>
              <td>{{ lot.location }}</td>
              <td>₹{{ lot.price }}</td>
              <td>{{ lot.total_spots }}</td>

              <td>
                <span class="tag-black">{{ lot.available_spots }}</span>
              </td>

              <td>
                <span class="tag-black">{{ lot.total_spots - lot.available_spots }}</span>
              </td>

              <td class="action-col">
                <button @click="openSpotModal(lot.lot_id)" class="btn-black">
                  View Spots
                </button>

                <router-link :to="`/admin/lots`" class="btn-black">
                  Edit
                </router-link>

                <button @click="deleteLot(lot.lot_id)" class="btn-black">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="!loading && lots.length === 0" class="empty-msg">
          No parking lots created yet.
        </div>
      </div>

      <!-- Users Table -->
      <div v-if="showUsers" class="table-card">
        <div class="card-title">Registered Users</div>

        <table v-if="users.length > 0" class="main-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Sessions</th>
              <th>Last Activity</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="u in users" :key="u.id">
              <td>{{ u.id }}</td>
              <td>{{ u.name }}</td>
              <td>{{ u.email }}</td>
              <td>{{ u.total_sessions }}</td>
              <td>{{ u.last_activity || "N/A" }}</td>
            </tr>
          </tbody>
        </table>

        <div v-else class="empty-msg">No users registered yet.</div>
      </div>

      <!-- Modal -->
      <div v-if="showSpotModal" class="modal-overlay">
        <div class="modal-box">
          <div class="modal-header">
            <h3>Spots – {{ currentLotName }}</h3>
            <button @click="closeSpotModal" class="modal-close">✕</button>
          </div>

          <table class="modal-table">
            <thead>
              <tr>
                <th>Spot</th>
                <th>Status</th>
                <th>Vehicle</th>
                <th>User</th>
                <th>Entry Time</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="s in spotDetails" :key="s.spot_id">
                <td>{{ s.spot_number }}</td>
                <td>
                  <span v-if="s.is_available" class="available-tag">Available</span>
                  <span v-else class="occupied-tag">Occupied</span>
                </td>

                <td>{{ s.vehicle_number || "-" }}</td>
                <td>{{ s.user_name || "-" }}</td>
                <td>{{ s.entry_time || "-" }}</td>
              </tr>
            </tbody>
          </table>

          <div v-if="spotDetails.length === 0" class="empty-msg">
            No spots found for this lot.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import { adminAPI } from "../services/api";

export default {
  setup() {
    const loading = ref(true);
    const lots = ref([]);
    const stats = ref({
      totalLots: 0,
      totalSpots: 0,
      occupiedSpots: 0,
      totalUsers: 0,
    });
    const users = ref([]);
    const showUsers = ref(false);

    const showSpotModal = ref(false);
    const spotDetails = ref([]);
    const currentLotName = ref("");

    const adminEmail = localStorage.getItem("admin_email");
    const adminPassword = localStorage.getItem("admin_password");

    const loadData = async () => {
      try {
        const lotsRes = await adminAPI.getLots(adminEmail, adminPassword);
        lots.value = lotsRes.data.lots || [];

        stats.value.totalLots = lots.value.length;
        stats.value.totalSpots = lots.value.reduce((s, l) => s + l.total_spots, 0);
        stats.value.occupiedSpots = lots.value.reduce(
          (s, l) => s + (l.total_spots - l.available_spots),
          0
        );

        const usersRes = await adminAPI.users(adminEmail, adminPassword);
        users.value = usersRes.data.users || [];
        stats.value.totalUsers = users.value.length;
      } catch (err) {
        console.error("Failed to load admin data:", err);
      } finally {
        loading.value = false;
      }
    };

    onMounted(loadData);

    const deleteLot = async (lotId) => {
      if (!confirm("Are you sure you want to delete this lot?")) return;

      try {
        await adminAPI.deleteLot(lotId, adminEmail, adminPassword);

        lots.value = lots.value.filter((l) => l.lot_id !== lotId);
      } catch (err) {
        alert("Failed: " + (err.response?.data?.error || "Unknown"));
      }
    };

    const openSpotModal = async (lotId) => {
      const lot = lots.value.find((l) => l.lot_id === lotId);
      currentLotName.value = lot ? lot.name : `Lot ${lotId}`;

      const res = await adminAPI.lotSpotStatus(lotId, adminEmail, adminPassword);
      spotDetails.value = res.data.spots || [];
      showSpotModal.value = true;
    };

    const closeSpotModal = () => {
      showSpotModal.value = false;
      spotDetails.value = [];
    };

    const statsCards = computed(() => [
      { label: "Total Parking Lots", value: stats.value.totalLots },
      { label: "Total Spots", value: stats.value.totalSpots },
      { label: "Occupied Spots", value: stats.value.occupiedSpots },
      { label: "Registered Users", value: stats.value.totalUsers },
    ]);

    return {
      loading,
      lots,
      stats,
      users,
      showUsers,

      statsCards,
      deleteLot,

      showSpotModal,
      spotDetails,
      currentLotName,
      openSpotModal,
      closeSpotModal,
    };
  },
};
</script>

<style scoped>
/* Main Background */
.dashboard-bg {
  min-height: 100vh;
  background: black;
  padding: 40px 0;
}

/* Container */
.main-container {
  max-width: 1200px;
  margin: auto;
}

/* Title */
.page-title {
  color: white;
  font-size: 2.3rem;
  font-weight: bold;
  margin-bottom: 26px;
}

/* Stats */
.stats-container {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
  margin-bottom: 35px;
}

.stat-card {
  flex: 1;
  min-width: 180px;
  background: black;
  border: 1px solid white;
  border-radius: 14px;
  padding: 22px 0;
  text-align: center;
  color: white;
  transition: 0.25s;
}

.stat-card:hover {
  background: white;
  color: black;
}

.stat-value {
  font-size: 2.4rem;
  font-weight: 800;
}

.stat-label {
  opacity: 0.9;
  margin-top: 6px;
}

/* ACTION BUTTONS ROW */
.action-buttons {
  display: flex;
  gap: 18px;          /* <<< GAP FIXED */
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.btn-white,
.btn-black {
  padding: 16px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  font-size: 1rem;
  transition: 0.25s;
  display: inline-block;
}

/* White Button */
.btn-white {
  background: white;
  color: black;
  border: 1px solid white;
}

.btn-white:hover {
  background: black;
  color: white;
  border-color: white;
}

/* Black Button */
.btn-black {
  background: black;
  color: white;
  border: 1px solid black;
}

.btn-black:hover {
  background: white;
  color: black;
  border-color: black;
}

/* Action column buttons spacing */
.action-col {
  display: flex;
  gap: 10px;        /* <<< Buttons inside table also spaced */
  justify-content: center;
}

/* Table Card */
.table-card {
  background: white;
  padding: 24px;
  border-radius: 18px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  margin-top: 25px;
}

.card-title {
  color: black;
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 14px;
}

/* Table */
.main-table {
  width: 100%;
  border-collapse: collapse;
}

.main-table th {
  padding: 13px 8px;
  background: #f3f4f6;
  border-bottom: 2px solid black;
}

.main-table td {
  padding: 10px;
  text-align: center;
}

.tag-black {
  background: black;
  color: white;
  padding: 6px 14px;
  border-radius: 6px;
  font-weight: 600;
}

/* Empty Message */
.empty-msg {
  text-align: center;
  padding: 30px;
  font-weight: 600;
  color: #6366f1;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
}

.modal-box {
  background: white;
  width: 90%;
  max-width: 800px;
  border-radius: 14px;
  padding: 20px;
  max-height: 80vh;
  overflow: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-close {
  background: black;
  color: white;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  border: none;
  cursor: pointer;
}

.modal-close:hover {
  background: white;
  color: black;
  border: 1px solid black;
}

/* Tags */
.available-tag {
  background: #16a34a;
  color: white;
  padding: 4px 10px;
  border-radius: 10px;
  font-size: 0.8rem;
}

.occupied-tag {
  background: #dc2626;
  color: white;
  padding: 4px 10px;
  border-radius: 10px;
  font-size: 0.8rem;
}

</style>
