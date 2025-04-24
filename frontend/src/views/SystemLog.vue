<template>
  <div class="systemlog-container">
    <div class="card-container">
      <el-card class="card">
        <template #header>
          <div class="card-header">
            <span>系统日志</span>
          </div>
        </template>
        <div class="card-body">
          <pre>{{ systemLog }}</pre>
        </div>
        <template #footer>
          <div class="card-footer">
            <el-button 
              @click="toggleAutoRefresh('system')" 
              :type="autoRefreshEnabled.system ? 'warning' : 'success'" 
              :disabled="!hasPermission"
              style="margin-right: 10px;"
            >
              {{ autoRefreshEnabled.system ? '关闭自动刷新' : '开启自动刷新' }}
            </el-button>
            <el-button 
              @click="clearLogs('system')" 
              type="danger" 
              :disabled="!hasPermission" 
              style="margin-left: 15px;"
            >
              清空日志
            </el-button>
          </div>
        </template>
      </el-card>
      <el-card class="card">
        <template #header>
          <div class="card-header">
            <span>爬虫日志</span>
          </div>
        </template>
        <div class="card-body">
          <pre>{{ crawlerLog }}</pre>
        </div>
        <template #footer>
          <div class="card-footer">
            <el-button 
              @click="toggleAutoRefresh('crawler')" 
              :type="autoRefreshEnabled.crawler ? 'warning' : 'success'" 
              :disabled="!hasPermission"
              style="margin-right: 10px;"
            >
              {{ autoRefreshEnabled.crawler ? '关闭自动刷新' : '开启自动刷新' }}
            </el-button>
            <el-button 
              @click="clearLogs('crawler')" 
              type="danger" 
              :disabled="!hasPermission" 
              style="margin-left: 15px;"
            >
              清空日志
            </el-button>
          </div>
        </template>
      </el-card>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "SystemLog",
  data() {
    return {
      systemLog: "",
      crawlerLog: "",
      autoRefreshEnabled: {
        system: true,
        crawler: true
      }, 
      intervalIds: {
        system: null,
        crawler: null
      }
    };
  },
  mounted() {
    this.fetchLogs('system');
    this.fetchLogs('crawler');
  },
  methods: {
    async fetchLogs(type) {
      const username = localStorage.getItem('username');
      try {
        const res = await axios.get(`http://127.0.0.1:8000/api/${type}log`, {
          params: { username }
        });
        this[`${type}Log`] = res.data;
      } catch (error) {
        if (error.response) {
          this.$message.error(error.response.data.detail);
        } else {
          this.$message.error('网络请求失败');
        }
      }
    },

    async clearLogs(type) {
      const username = localStorage.getItem('username');
      try {
        const res = await axios.get(`http://127.0.0.1:8000/api/de${type}log`, {
          params: { username }
        });
        this[`${type}Log`] = "";
        this.$message.success(res.data.message);
      } catch (error) {
        if (error.response) {
          this.$message.error(error.response.data.detail);
        } else {
          this.$message.error('网络请求失败！');
        }
      }
    },

    toggleAutoRefresh(type) {
      this.autoRefreshEnabled[type] = !this.autoRefreshEnabled[type];
      
      if (this.autoRefreshEnabled[type]) {
        this.fetchLogs(type);
        this.intervalIds[type] = setInterval(() => this.fetchLogs(type), 100000);
      } else {
        clearInterval(this.intervalIds[type]);
      }
    }
  },
  beforeUnmount() {
    clearInterval(this.intervalIds.system);
    clearInterval(this.intervalIds.crawler);
  },
  computed: {
    hasPermission() {
      return !!localStorage.getItem('username');
    }
  }
};
</script>


<style scoped>
.systemlog-container {
  padding: 20px;
}

.card-container {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.card {
  flex: 1 1 45%;
  min-width: 300px;
}

.card-body {
  white-space: pre-wrap;
  word-break: break-all;
  font-family: monospace;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
  max-height: 400px;
  overflow-y: auto;
}

.card-footer {
  text-align: center;
  padding-top: 5px;
}
</style>