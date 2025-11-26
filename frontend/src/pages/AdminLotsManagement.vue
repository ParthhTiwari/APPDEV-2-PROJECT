<!-- filepath: frontend/src/pages/AdminLotsManagement.vue -->
<template>
  <div class="container mt-5">
    <h1 class="mb-4">🏢 Manage Parking Lots</h1>

    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else class="row">
      <div v-for="lot in lots" :key="lot.lot_id" class="col-md-4 mb-4">
        <div class="card shadow">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">{{ lot.name }}</h5>
          </div>
          <div class="card-body">
            <p><strong>Location:</strong> {{ lot.location }}</p>
            <p><strong>Price/Hour:</strong> ₹{{ lot.price }}</p>
            <p><strong>Total Spots:</strong> {{ lot.total_spots }}</p>
            <p>
              <strong>Available:</strong> 
              <span class="badge bg-success">{{ lot.available_spots }}</span>
            </p>
            <p>
              <strong>Occupied:</strong> 
              <span class="badge bg-danger">{{ lot.total_spots - lot.available_spots }}</span>
            </p>
          </div>
          <div class="card-footer">
            <button @click="editLot(lot.lot_id)" class="btn btn-sm btn-primary">
              ✏️ Edit
            </button>
            <button @click="deleteLot(lot.lot_id)" class="btn btn-sm btn-danger ms-1">
              🗑️ Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <router-link to="/admin/dashboard" class="btn btn-secondary mt-4">
      ← Back to Dashboard
    </router-link>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { adminAPI } from '../services/api';

export default {
  setup() {
    const loading = ref(true);
    const lots = ref([]);

    const adminEmail = localStorage.getItem('admin_email');
    const adminPassword = localStorage.getItem('admin_password');

    onMounted(async () => {
      try {
        const response = await adminAPI.getLots(adminEmail, adminPassword);
        lots.value = response.data.lots || [];
      } catch (err) {
        console.error('Failed to load lots:', err);
      } finally {
        loading.value = false;
      }
    });

    const editLot = (lotId) => {
      alert('Edit functionality coming soon for lot ' + lotId);
    };

    const deleteLot = async (lotId) => {
      if (confirm('Are you sure? This lot will be deleted.')) {
        try {
          await adminAPI.deleteLot(lotId, adminEmail, adminPassword);
          lots.value = lots.value.filter(lot => lot.lot_id !== lotId);
        } catch (err) {
          alert('Failed to delete: ' + (err.response?.data?.error || 'Unknown error'));
        }
      }
    };

    return {
      loading,
      lots,
      editLot,
      deleteLot
    };
  }
};
</script>