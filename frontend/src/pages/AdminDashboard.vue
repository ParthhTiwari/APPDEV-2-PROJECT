<!-- filepath: frontend/src/pages/AdminDashboard.vue -->
<template>
  <div class="container mt-5">
    <div class="row">
      <div class="col-md-12">
        <h1 class="mb-4">📊 Admin Dashboard</h1>
        
        <!-- Stats Cards -->
        <div class="row mb-4">
          <div class="col-md-3">
            <div class="card bg-primary text-white shadow">
              <div class="card-body text-center">
                <h2>{{ stats.totalLots }}</h2>
                <p>Total Parking Lots</p>
              </div>
            </div>
          </div>
          
          <div class="col-md-3">
            <div class="card bg-success text-white shadow">
              <div class="card-body text-center">
                <h2>{{ stats.totalSpots }}</h2>
                <p>Total Spots</p>
              </div>
            </div>
          </div>
          
          <div class="col-md-3">
            <div class="card bg-warning text-white shadow">
              <div class="card-body text-center">
                <h2>{{ stats.occupiedSpots }}</h2>
                <p>Occupied Spots</p>
              </div>
            </div>
          </div>
          
          <div class="col-md-3">
            <div class="card bg-info text-white shadow">
              <div class="card-body text-center">
                <h2>{{ stats.totalUsers }}</h2>
                <p>Registered Users</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="row mb-4">
          <div class="col-md-12">
            <router-link to="/admin/create-lot" class="btn btn-success me-2">
              ➕ Create New Lot
            </router-link>
            <router-link to="/admin/lots" class="btn btn-primary">
              🏢 Manage Lots
            </router-link>
          </div>
        </div>

        <!-- Parking Lots Table -->
        <div class="card shadow">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">🅿️ All Parking Lots</h5>
          </div>
          <div class="card-body">
            <div v-if="loading" class="text-center">
              <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
            
            <table v-else class="table table-hover">
              <thead class="table-light">
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
                  <td><span class="badge bg-success">{{ lot.available_spots }}</span></td>
                  <td><span class="badge bg-danger">{{ lot.total_spots - lot.available_spots }}</span></td>
                  <td>
                    <router-link :to="`/admin/lots`" class="btn btn-sm btn-primary">
                      Edit
                    </router-link>
                    <button @click="deleteLot(lot.lot_id)" class="btn btn-sm btn-danger ms-1">
                      Delete
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
            
            <div v-if="!loading && lots.length === 0" class="alert alert-info">
              No parking lots created yet.
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { adminAPI } from '../services/api';

export default {
  setup() {
    const loading = ref(true);
    const lots = ref([]);
    const stats = ref({
      totalLots: 0,
      totalSpots: 0,
      occupiedSpots: 0,
      totalUsers: 0
    });

    const adminEmail = localStorage.getItem('admin_email');
    const adminPassword = localStorage.getItem('admin_password');

    onMounted(async () => {
      try {
        const response = await adminAPI.getLots(adminEmail, adminPassword);
        lots.value = response.data.lots || [];
        
        // Calculate stats
        stats.value.totalLots = lots.value.length;
        stats.value.totalSpots = lots.value.reduce((sum, lot) => sum + lot.total_spots, 0);
        stats.value.occupiedSpots = lots.value.reduce((sum, lot) => 
          sum + (lot.total_spots - lot.available_spots), 0
        );
      } catch (err) {
        console.error('Failed to load lots:', err);
      } finally {
        loading.value = false;
      }
    });

    const deleteLot = async (lotId) => {
      if (confirm('Are you sure you want to delete this lot?')) {
        try {
          await adminAPI.deleteLot(lotId, adminEmail, adminPassword);
          lots.value = lots.value.filter(lot => lot.lot_id !== lotId);
        } catch (err) {
          alert('Failed to delete lot: ' + (err.response?.data?.error || 'Unknown error'));
        }
      }
    };

    return {
      loading,
      lots,
      stats,
      deleteLot
    };
  }
};
</script>