<template>
  <div class="hot-analysis">
    <el-tabs type="card" v-model="activeTab" @tab-change="handleTabChange">
        <el-tab-pane label="微博热门分析" name="wbhot"></el-tab-pane>
        <el-tab-pane label="百度热门分析" name="bdhot"></el-tab-pane>
        <el-tab-pane label="B站热门分析" name="blhot"></el-tab-pane>
    </el-tabs>
    <el-button type="primary" @click="refreshImages" style="position: absolute; right: 50px; top: 30px;">刷新</el-button>
    <div class="refresh-time" style="color: burlywood; font-size: 15px; position: absolute; right: 120px; top: 40px;">
      <span>上次刷新时间：{{ refreshTime }}</span>
    </div>
    <div class="hotwordcloud" style="margin-top: 20px;">
      <el-tooltip
        effect="light"
        content="基于爬取结果(共90条)"
        placement="right-end"
      >
        <span>热门词云图</span> 
      </el-tooltip>
    </div>
    <el-image
      loading="lazy"
      style="width: 400px; height: 200px; margin-top: 20px;"
      :src="currentWordCloud"
      fit="contain"
      :preview-src-list=[currentWordCloud]
    />
    <div class="hotsentiment" style="margin-top: 20px;">
      <el-tooltip
        effect="light"
        content="基于爬取结果(共30条)"
        placement="right-end"
      >
        <span>热门情感分析图</span>
      </el-tooltip>
    </div>
    <el-image
      loading="lazy"
      style="width: 300px; height: 300px; margin-top: 20px;"
      :src="currentSentiment"
      fit="contain"
      :preview-src-list=[currentSentiment]
    />
  </div>
</template>


<script>

export default {

  data() {
    return {
      activeTab: 'wbhot',  
      refreshTime: '',
      currentWordCloud: '', 
      currentSentiment: '' 
    };
  },
  
  watch: {
    activeTab(newVal) {
      this.fetchImages(newVal);
    }
  },

  methods: {
    async fetchImages(platform) {
      const username = localStorage.getItem('username') || '';
      this.currentWordCloud = `http://127.0.0.1:8000/api/${platform}wordcloud?username=${username}`;
      this.currentSentiment = `http://127.0.0.1:8000/api/${platform}sentiment?username=${username}`;
    },
    async refreshImages() {
      this.fetchImages(this.activeTab);
      this.refreshTime = new Date().toLocaleString();
      this.$message.success('刷新成功');
    },
    async handleTabChange(tabName) {
      this.fetchImages(tabName);
    },
  },
  
  mounted() {
    this.fetchImages(this.activeTab);
    this.refreshTime = new Date().toLocaleString();
  }
};
</script>