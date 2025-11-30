<template>
  <div class="export-container">
    <div class="export-card">
      <div class="card-header">
        <h4>📥 Export Your Parking Data</h4>
      </div>

      <div class="card-body">
        <p class="desc">
          Download your complete parking history as a CSV file. Click the
          button below to start the export.
        </p>

        <button
          @click="startExport"
          class="primary-btn"
          :disabled="exporting || downloadReady"
        >
          {{
            exporting
              ? "Processing..."
              : downloadReady
              ? "✅ Ready"
              : "📥 Start Export"
          }}
        </button>

        <div v-if="taskId" class="status-box">
          <div class="task-id">
            <strong>Task ID:</strong> {{ taskId }}
          </div>

          <div class="progress-bar">
            <div
              class="progress-fill"
              :style="{ width: progressPercent + '%' }"
            ></div>
          </div>

          <p class="center status-label">
            <strong>Status:</strong>
            <span
              v-if="status === 'processing'"
              class="badge warning"
            >
              ⏳ Processing
            </span>
            <span
              v-else-if="status === 'success'"
              class="badge success"
            >
              ✅ Ready
            </span>
            <span v-else class="badge grey">
              {{ status }}
            </span>
          </p>

          <button
            v-if="downloadReady"
            @click="downloadFile"
            class="primary-btn"
          >
            📥 Download CSV
          </button>
        </div>

        <div v-if="error" class="error-box">
          {{ error }}
        </div>
      </div>

      <router-link to="/user/dashboard" class="back-btn">
        ← Back to Dashboard
      </router-link>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { userAPI } from "../services/api";

export default {
  setup() {
    const userId = localStorage.getItem("user_id");
    const exporting = ref(false);
    const taskId = ref(null);
    const status = ref(null);
    const downloadReady = ref(false);
    const error = ref("");
    const progressPercent = ref(0);

    const startExport = async () => {
      exporting.value = true;
      error.value = "";
      downloadReady.value = false;
      progressPercent.value = 0;

      try {
        const response = await userAPI.exportHistory(userId);
        taskId.value = response.data.task_id;
        status.value = "processing";
        pollStatus();
      } catch (err) {
        error.value =
          err.response?.data?.error || "Failed to start export";
        exporting.value = false;
      }
    };

    const pollStatus = async () => {
      if (!taskId.value) return;

      try {
        const response = await userAPI.exportStatus(taskId.value);
        status.value = response.data.status;

        if (status.value === "SUCCESS") {
          downloadReady.value = true;
          exporting.value = false;
          progressPercent.value = 100;
        } else if (
          status.value === "PENDING" ||
          status.value === "PROCESSING"
        ) {
          progressPercent.value = Math.min(
            90,
            progressPercent.value + 10
          );
          setTimeout(pollStatus, 1000);
        }
      } catch (err) {
        console.error("Poll error:", err);
      }
    };

    const downloadFile = async () => {
      try {
        const response = await userAPI.downloadExport(taskId.value);
        const blob = new Blob([response.data], {
          type: "text/csv",
        });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download =
          "parking_history_" +
          new Date().toISOString().split("T")[0] +
          ".csv";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      } catch {
        error.value = "Failed to download file";
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
      downloadFile,
    };
  },
};
</script>

<style scoped>
.export-container {
  display: flex;
  justify-content: center;
  padding: 30px;
  background: black;               /* Full black BG */
  min-height: 100vh;
}

.export-card {
  width: 100%;
  max-width: 650px;
  background: #0e0e0e;             /* Dark card */
  border: 1px solid white;         /* White border */
  border-radius: 16px;
  padding: 24px;
  color: white;                    /* White text */
}

/* ===== Card Header ===== */
.card-header {
  padding: 16px;
  border-radius: 12px;
  text-align: center;
  margin-bottom: 22px;
  border: 1px solid white;
  background: rgba(255, 255, 255, 0.05);
}

.card-header h4 {
  margin: 0;
  font-size: 22px;
  color: white;
}

/* ===== Description ===== */
.desc {
  color: #ccc;
  font-size: 15px;
  margin-bottom: 22px;
}

/* ===== Buttons ===== */
.primary-btn {
  width: 100%;
  background: transparent;
  color: white;
  font-size: 17px;
  padding: 12px;
  border: 1px solid white;
  border-radius: 10px;
  cursor: pointer;
  transition: 0.3s;
}

.primary-btn:hover {
  background: white;
  color: black;
}

.primary-btn:disabled {
  background: rgba(255,255,255,0.2);
  border-color: rgba(255,255,255,0.3);
  cursor: not-allowed;
}

/* ===== Status Box ===== */
.status-box {
  margin-top: 25px;
}

.task-id {
  background: rgba(255,255,255,0.1);
  padding: 12px;
  border-radius: 10px;
  margin-bottom: 18px;
  font-size: 14px;
  border: 1px solid white;
}

/* ===== Progress Bar ===== */
.progress-bar {
  width: 100%;
  height: 12px;
  background: rgba(255,255,255,0.1);
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 15px;
  border: 1px solid white;
}

.progress-fill {
  height: 100%;
  background: white;
  transition: width 0.4s ease;
}

/* ===== Badges ===== */
.badge {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 14px;
}

.warning {
  background: #ff9800;
  color: black;
}

.success {
  background: #28a745;
  color: white;
}

.grey {
  background: grey;
  color: white;
}

/* ===== Error Box ===== */
.error-box {
  background: rgba(255, 0, 0, 0.15);
  color: #ff6b6b;
  padding: 12px;
  border-radius: 10px;
  margin-top: 18px;
  border: 1px solid red;
}

/* ===== Back Button ===== */
.back-btn {
  display: inline-block;
  margin-top: 24px;
  text-decoration: none;
  color: white;
  font-size: 16px;
  border: 1px solid white;
  padding: 10px 14px;
  border-radius: 8px;
  transition: 0.3s;
}

.back-btn:hover {
  background: white;
  color: black;
}
</style>
