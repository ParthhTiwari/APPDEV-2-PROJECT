<!-- filepath: frontend/src/pages/UserExportHistory.vue -->
<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow">
          <div class="card-header bg-info text-white">
            <h4 class="mb-0">📥 Export Your Parking Data</h4>
          </div>
          <div class="card-body">
            <p class="text-muted">
              Download your complete parking history as a CSV file. Click the button below to start the export.
            </p>

            <!-- Export Button -->
            <button 
              @click="startExport" 
              class="btn btn-success btn-lg w-100"
              :disabled="exporting || downloadReady"
            >
              {{ exporting ? 'Processing...' : downloadReady ? '✅ Ready' : '📥 Start Export' }}
            </button>

            <!-- Status Section -->
            <div v-if="taskId" class="mt-4">
              <div class="alert alert-info">
                <strong>Task ID:</strong> {{ taskId }}
              </div>

              <div class="progress mb-3">
                <div 
                  class="progress-bar progress-bar-animated" 
                  :style="{ width: progressPercent + '%' }"
                  role="progressbar"
                ></div>
              </div>

              <p class="text-center">
                <strong>Status:</strong> 
                <span v-if="status === 'processing'" class="badge bg-warning">⏳ Processing</span>
                <span v-else-if="status === 'success'" class="badge bg-success">✅ Ready</span>
                <span v-else class="badge bg-secondary">{{ status }}</span>
              </p>

              <!-- Download Button -->
              <button 
                v-if="downloadReady" 
                @click="downloadFile" 
                class="btn btn-primary btn-lg w-100"
              >
                📥 Download CSV
              </button>
            </div>

            <!-- Error -->
            <div v-if="error" class="alert alert-danger mt-3">
              {{ error }}
            </div>
          </div>
        </div>

        <router-link to="/user/dashboard" class="btn btn-secondary mt-4">
          ← Back to Dashboard
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { userAPI } from '../services/api';

export default {
  setup() {
    const userId = localStorage.getItem('user_id');
    const exporting = ref(false);
    const taskId = ref(null);
    const status = ref(null);
    const downloadReady = ref(false);
    const error = ref('');
    const progressPercent = ref(0);

    const startExport = async () => {
      exporting.value = true;
      error.value = '';

      try {
        const response = await userAPI.exportHistory(userId);
        taskId.value = response.data.task_id;
        status.value = 'processing';

        // Poll for status
        pollStatus();
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to start export';
        exporting.value = false;
      }
    };

    const pollStatus = async () => {
      if (!taskId.value) return;

      try {
        const response = await userAPI.exportStatus(taskId.value);
        status.value = response.data.status;

        if (status.value === 'SUCCESS') {
          downloadReady.value = true;
          progressPercent.value = 100;
        } else if (status.value === 'PENDING' || status.value === 'PROCESSING') {
          progressPercent.value = Math.min(90, progressPercent.value + 10);
          // Poll again after 1 second
          setTimeout(pollStatus, 1000);
        }
      } catch (err) {
        console.error('Poll error:', err);
      }
    };

    const downloadFile = async () => {
      try {
        const response = await userAPI.downloadExport(taskId.value);
        
        // Create blob and download
        const blob = new Blob([response.data], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `parking_history_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      } catch (err) {
        error.value = 'Failed to download file';
      }
    };

    return {
      userId,
      exporting,
      taskId,
      status,
      downloadReady,
      error,
      progressPercent,
      startExport,
      downloadFile
    };
  }
};
</script>