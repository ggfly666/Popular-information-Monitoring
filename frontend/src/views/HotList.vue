<template>
    <div class="hot-list-container">
      <el-tabs type="card" v-model="activeTab" @tab-change="handleTabChange">
        <el-tab-pane label="微博热门" name="wb"></el-tab-pane>
        <el-tab-pane label="百度热门" name="bd"></el-tab-pane>
        <el-tab-pane label="B站热门" name="bl"></el-tab-pane>  
      </el-tabs>
      <el-table 
        :data="currentData"  
        v-loading="loading"
        @row-click="handleRowClick"
      >
        <el-table-column prop="ranking" label="排名" width="80"></el-table-column>
        <el-table-column prop="info" label="热门信息">
        </el-table-column>
        <el-table-column prop="hot" label="热度" width="120"></el-table-column>
        <el-table-column prop="uptime" label="更新时间" width="180">
        </el-table-column>
      </el-table>
      <div class="refresh-button">
        <el-button 
          type="primary"  
          @click="refreshCurrentTab"
          style="position: absolute; right: 50px; top: 30px;"
          >
          刷新
        </el-button>
        <div class="refresh-time" style="color: burlywood; font-size: 15px; position: absolute; right: 120px; top: 40px;">
        <span>上次刷新时间：{{ refreshTime }}</span>
        </div>
      </div>
    </div>
</template>
  
<script>
import axios from 'axios';

export default {
  data() {
    return {
      activeTab: 'wb',
      refreshTime: '',
      wbData: [],
      bdData: [],
      blData: [],
      loading: false,
    };
  },
  computed: {
    currentData() {
      return this[`${this.activeTab}Data`]; 
    }
  },
  methods: {
    async fetchHotInfo(platform) {
      const username = localStorage.getItem('username');
      this.loading = true;
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/${platform}hotinfo`, {
          params: { username }
        });
        this[`${platform}Data`] = response.data;
        this.total = response.data.length;
      } catch (error) {
        this.$message.error(
              error.response.data.detail
        );
      } finally {
        this.loading = false;
      }
    },
    async handleTabChange(tabName) {
      this.fetchHotInfo(tabName);
    },
    async handleRowClick(row) {
      if (row.url){
        window.open(row.url);
      }
    },
    async refreshCurrentTab() {
      this.fetchHotInfo(this.activeTab);
      this.refreshTime = new Date().toLocaleString(); 
      this.$message.success('刷新成功');
    },
  },
  mounted() {
    this.fetchHotInfo('wb');
    this.refreshTime = new Date().toLocaleString();
  }
};
</script>

<style scoped>
.hot-list-container {
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}
.tabs-container {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  position: relative;
}
</style>