<!-- filepath: frontend/src/pages/AdminCreateLot.vue -->
<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-header bg-success text-white">
            <h4 class="mb-0">➕ Create Parking Lot</h4>
          </div>
          <div class="card-body">
            <form @submit.prevent="createLot">
              <div class="mb-3">
                <label class="form-label">Lot Name</label>
                <input 
                  v-model="form.name" 
                  type="text" 
                  class="form-control"
                  placeholder="e.g., Downtown Parking"
                  required
                >
              </div>

              <div class="mb-3">
                <label class="form-label">Location</label>
                <input 
                  v-model="form.location" 
                  type="text" 
                  class="form-control"
                  placeholder="e.g., Main Street, City"
                  required
                >
              </div>

              <div class="mb-3">
                <label class="form-label">Price per Hour (₹)</label>
                <input 
                  v-model.number="form.price" 
                  type="number" 
                  class="form-control"
                  placeholder="e.g., 50"
                  step="0.01"
                  required
                >
              </div>

              <div class="mb-3">
                <label class="form-label">Number of Spots</label>
                <input 
                  v-model.number="form.max_spots" 
                  type="number" 
                  class="form-control"
                  placeholder="e.g., 100"
                  min="1"
                  required
                >
              </div>

              <button type="submit" class="btn btn-success w-100" :disabled="loading">
                {{ loading ? 'Creating...' : 'Create Lot' }}
              </button>
            </form>

            <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
            <div v-if="success" class="alert alert-success mt-3">{{ success }}</div>
          </div>
        </div>

        <router-link to="/admin/dashboard" class="btn btn-secondary mt-3">
          ← Back to Dashboard
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { adminAPI } from '../services/api';

export default {
  setup() {
    const router = useRouter();
    const loading = ref(false);
    const error = ref('');
    const success = ref('');

    const form = ref({
      name: '',
      location: '',
      price: '',
      max_spots: ''
    });

    const adminEmail = localStorage.getItem('admin_email');
    const adminPassword = localStorage.getItem('admin_password');

    const createLot = async () => {
      loading.value = true;
      error.value = '';
      success.value = '';

      try {
        const response = await adminAPI.createLot(form.value, adminEmail, adminPassword);
        success.value = response.data.message || 'Lot created successfully!';
        
        form.value = { name: '', location: '', price: '', max_spots: '' };
        
        setTimeout(() => {
          router.push('/admin/dashboard');
        }, 1500);
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to create lot';
      } finally {
        loading.value = false;
      }
    };

    return {
      form,
      loading,
      error,
      success,
      createLot
    };
  }
};
</script>