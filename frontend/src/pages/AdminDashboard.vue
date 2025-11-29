<template>
  <div class="dashboard-bg">
    <div style="max-width:1200px; margin:40px auto;">
      <h1
        style="
          font-size:2.1rem;
          font-weight:bold;
          margin-bottom:30px;
          display:flex;
          align-items:center;
        "
      >
        <span style="font-size:2.4rem; margin-right:12px;">
          <h1 style="color:white">Admin Dashboard</h1>
        </span>
      </h1>

      <div
        style="
          display:flex;
          gap:24px;
          margin-bottom:38px;
          flex-wrap:wrap;
        "
      >
        <div
          v-for="card in statsCards"
          :key="card.label"
          :style="`flex:1; min-width:180px; background:${card.bg}; color:white; border-radius:14px; border:1px solid white; padding:22px 0; text-align:center;`"
        >
          <div style="font-size:2.4rem; font-weight:800;">
            {{ card.value }}
          </div>
          <div style="opacity:0.9; margin-top:6px;">
            {{ card.label }}
          </div>
        </div>
      </div>

      <div style="margin-bottom:26px;">
        <router-link
          to="/admin/create-lot"
          style="
            background:white;
            color:black;
            padding:11px 24px;
            text-decoration:none;
            border-radius:6px;
            font-weight:600;
            margin-right:18px;
            font-size:1rem;
          "
        >
          ➕ Create New Lot
        </router-link>

        <router-link
          to="/admin/lots"
          style="
            background:white;
            color:black;
            padding:11px 24px;
            text-decoration:none;
            border-radius:6px;
            font-weight:600;
            font-size:1rem;
          "
        >
          🏢 Manage Lots
        </router-link>

        <button
          @click="showUsers = !showUsers"
          style="
            background:white;
            color:black;
            padding:11px 24px;
            text-decoration:none;
            border-radius:6px;
            font-weight:600;
            margin-left:18px;
            font-size:1rem;
            cursor:pointer;
          "
        >
          👥 Show Registered Users
        </button>
      </div>

      <div
        style="
          background:#fff;
          border-radius:18px;
          box-shadow:0 2px 12px rgba(0,0,0,0.09);
          padding:24px;
        "
      >
        <div
          style="
            font-size:1.2rem;
            font-weight:600;
            margin-bottom:16px;
            color:black;
          "
        >
          All Parking Lots
        </div>

        <div v-if="loading" style="text-align:center; padding:40px 0;">
          <span style="font-size:1.4rem;">Loading...</span>
        </div>

        <table v-else style="width:100%; border-collapse:collapse;">
          <thead>
            <tr
              style="
                background:#f3f4f6;
                color:#23272a;
                font-size:1.07rem;
              "
            >
              <th style="padding:13px 8px; border-bottom:2px solid black;">
                ID
              </th>
              <th style="padding:13px 8px; border-bottom:2px solid black;">
                Name
              </th>
              <th style="padding:13px 8px; border-bottom:2px solid black;">
                Location
              </th>
              <th style="padding:13px 8px; border-bottom:2px solid black;">
                Price/Hour
              </th>
              <th style="padding:13px 8px; border-bottom:2px solid black;">
                Total Spots
              </th>
              <th style="padding:13px 8px; border-bottom:2px solid black;">
                Available
              </th>
              <th style="padding:13px 8px; border-bottom:2px solid black;">
                Occupied
              </th>
              <th style="padding:13px 8px; border-bottom:2px solid black;">
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="lot in lots"
              :key="lot.lot_id"
              style="text-align:center; font-size:1rem;"
            >
              <td style="padding:8px;">{{ lot.lot_id }}</td>
              <td style="padding:8px;">{{ lot.name }}</td>
              <td style="padding:8px;">{{ lot.location }}</td>
              <td style="padding:8px;">₹{{ lot.price }}</td>
              <td style="padding:8px;">{{ lot.total_spots }}</td>
              <td style="padding:8px;">
                <span
                  style="
                    background:black;
                    color:white;
                    border-radius:4px;
                    font-weight:600;
                    padding:6px 14px;
                  "
                >
                  {{ lot.available_spots }}
                </span>
              </td>
              <td style="padding:8px;">
                <span
                  style="
                    background:black;
                    color:white;
                    border-radius:4px;
                    font-weight:600;
                    padding:6px 14px;
                  "
                >
                  {{ lot.total_spots - lot.available_spots }}
                </span>
              </td>
              <td style="padding:8px;">
                <button
                  @click="openSpotModal(lot.lot_id)"
                  style="
                    background:black;
                    color:white;
                    border:none;
                    border-radius:3px;
                    font-size:0.98em;
                    padding:7px 15px;
                    margin-right:6px;
                    cursor:pointer;
                  "
                >
                  View Spots
                </button>

                <router-link
                  :to="`/admin/lots`"
                  style="
                    background:black;
                    color:white;
                    border:none;
                    border-radius:3px;
                    font-size:0.98em;
                    padding:7px 15px;
                    margin-right:6px;
                    text-decoration:none;
                  "
                >
                  Edit
                </router-link>

                <button
                  @click="deleteLot(lot.lot_id)"
                  style="
                    background:black;
                    color:white;
                    border:none;
                    border-radius:3px;
                    font-size:0.98em;
                    padding:7px 15px;
                    cursor:pointer;
                  "
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <div
          v-if="!loading && lots.length === 0"
          style="
            color:#6366f1;
            font-weight:500;
            padding:35px 0;
            text-align:center;
          "
        >
          No parking lots created yet.
        </div>
      </div>

      <div
        v-if="showUsers"
        style="
          background:#fff;
          border-radius:18px;
          box-shadow:0 2px 12px rgba(0,0,0,0.09);
          padding:24px;
          margin-top:32px;
        "
      >
        <div
          style="
            font-size:1.2rem;
            font-weight:600;
            margin-bottom:16px;
            color:black;
          "
        >
          Registered Users
        </div>

        <div v-if="users.length === 0">
          No users registered yet.
        </div>

        <table v-else style="width:100%; border-collapse:collapse;">
          <thead>
            <tr
              style="
                background:#f3f4f6;
                color:#23272a;
                font-size:1.07rem;
              "
            >
              <th style="padding:13px 8px; border-bottom:2px solid black;">
                ID
              </th>
              <th style="padding:13px 8px; border-bottom:2px solid black;">
                Name
              </th>
              <th style="padding:13px 8px; border-bottom:2px solid black;">
                Email
              </th>
              <th style="padding:13px 8px; border-bottom:2px solid black;">
                Sessions
              </th>
              <th style="padding:13px 8px; border-bottom:2px solid black;">
                Last Activity
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="u in users"
              :key="u.id"
              style="text-align:center; font-size:1rem;"
            >
              <td style="padding:8px;">{{ u.id }}</td>
              <td style="padding:8px;">{{ u.name }}</td>
              <td style="padding:8px;">{{ u.email }}</td>
              <td style="padding:8px;">{{ u.total_sessions }}</td>
              <td style="padding:8px;">{{ u.last_activity || "N/A" }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div
        v-if="showSpotModal"
        style="
          position:fixed;
          inset:0;
          background:rgba(0,0,0,0.6);
          display:flex;
          justify-content:center;
          align-items:center;
          z-index:50;
        "
      >
        <div
          style="
            background:white;
            width:90%;
            max-width:800px;
            border-radius:14px;
            padding:20px 22px;
            max-height:80vh;
            overflow:auto;
          "
        >
          <div
            style="
              display:flex;
              justify-content:space-between;
              align-items:center;
              margin-bottom:12px;
            "
          >
            <h3 style="margin:0; font-size:1.3rem;">
              Spots – {{ currentLotName }}
            </h3>
            <button
              @click="closeSpotModal"
              style="
                border:none;
                background:#111;
                color:white;
                border-radius:50%;
                width:30px;
                height:30px;
                cursor:pointer;
              "
            >
              ✕
            </button>
          </div>

          <table style="width:100%; border-collapse:collapse;">
            <thead>
              <tr style="background:#f3f4f6;">
                <th style="padding:8px; border-bottom:1px solid #ccc;">
                  Spot
                </th>
                <th style="padding:8px; border-bottom:1px solid #ccc;">
                  Status
                </th>
                <th style="padding:8px; border-bottom:1px solid #ccc;">
                  Vehicle
                </th>
                <th style="padding:8px; border-bottom:1px solid #ccc;">
                  User
                </th>
                <th style="padding:8px; border-bottom:1px solid #ccc;">
                  Entry Time
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="s in spotDetails"
                :key="s.spot_id"
                style="text-align:center; font-size:0.95rem;"
              >
                <td style="padding:6px 4px;">{{ s.spot_number }}</td>
                <td style="padding:6px 4px;">
                  <span
                    v-if="s.is_available"
                    style="
                      background:#16a34a;
                      color:white;
                      padding:3px 10px;
                      border-radius:10px;
                      font-size:0.8rem;
                    "
                  >
                    Available
                  </span>
                  <span
                    v-else
                    style="
                      background:#dc2626;
                      color:white;
                      padding:3px 10px;
                      border-radius:10px;
                      font-size:0.8rem;
                    "
                  >
                    Occupied
                  </span>
                </td>
                <td style="padding:6px 4px;">
                  {{ s.vehicle_number || "-" }}
                </td>
                <td style="padding:6px 4px;">
                  {{ s.user_name || "-" }}
                </td>
                <td style="padding:6px 4px;">
                  {{ s.entry_time || "-" }}
                </td>
              </tr>
            </tbody>
          </table>

          <div
            v-if="spotDetails.length === 0"
            style="margin-top:12px; text-align:center;"
          >
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
        const lotsRes = await adminAPI.getLots(
          adminEmail,
          adminPassword
        );
        lots.value = lotsRes.data.lots || [];
        stats.value.totalLots = lots.value.length;
        stats.value.totalSpots = lots.value.reduce(
          (s, l) => s + l.total_spots,
          0
        );
        stats.value.occupiedSpots = lots.value.reduce(
          (s, l) => s + (l.total_spots - l.available_spots),
          0
        );

        const usersRes = await adminAPI.users(
          adminEmail,
          adminPassword
        );
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
        stats.value.totalLots = lots.value.length;
        stats.value.totalSpots = lots.value.reduce(
          (s, l) => s + l.total_spots,
          0
        );
        stats.value.occupiedSpots = lots.value.reduce(
          (s, l) => s + (l.total_spots - l.available_spots),
          0
        );
      } catch (err) {
        alert(
          "Failed: " + (err.response?.data?.error || "Unknown")
        );
      }
    };

    const openSpotModal = async (lotId) => {
      try {
        const lot = lots.value.find((l) => l.lot_id === lotId);
        currentLotName.value = lot ? lot.name : `Lot ${lotId}`;

        const res = await adminAPI.lotSpotStatus(
          lotId,
          adminEmail,
          adminPassword
        );
        spotDetails.value = res.data.spots || [];
        showSpotModal.value = true;
      } catch {
        alert("Failed to load spots");
      }
    };

    const closeSpotModal = () => {
      showSpotModal.value = false;
      spotDetails.value = [];
    };

    const statsCards = computed(() => [
      {
        label: "Total Parking Lots",
        value: stats.value.totalLots,
        bg: "black",
      },
      {
        label: "Total Spots",
        value: stats.value.totalSpots,
        bg: "black",
      },
      {
        label: "Occupied Spots",
        value: stats.value.occupiedSpots,
        bg: "black",
      },
      {
        label: "Registered Users",
        value: stats.value.totalUsers,
        bg: "black",
      },
    ]);

    return {
      loading,
      lots,
      stats,
      users,
      showUsers,
      deleteLot,
      statsCards,
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
.dashboard-bg {
  min-height: 100vh;
  padding: 40px 0;
  background: black;
}
</style>
