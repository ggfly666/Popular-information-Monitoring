<template>
    <el-card style="max-width: 600px; margin-top: 50px;">
        <template #header>
            <div class="card-header">
                <span>爬虫爬取频率管理</span>
            </div>
        </template>
        <el-form :model="form" label-width="auto" style="max-width: 600px">
            <el-form-item label="微博爬虫爬取频率/h">
                <el-input-number v-model="form.Wbtime" :min="1" />
            </el-form-item>
            <el-form-item label="百度爬虫爬取频率/h">
                <el-input-number v-model="form.Bdtime" :min="1" />
            </el-form-item>
            <el-form-item label="B站爬虫爬取频率/h">
                <el-input-number v-model="form.Bltime" :min="1" />
            </el-form-item>
        </el-form>
        <template #footer>
            <div style="text-align: center;">
                <el-button type="primary" @click="getCrawlTime">刷新时间</el-button>
                <el-button type="primary" @click="updateCrawlTime">修改时间</el-button>
            </div>
        </template>
    </el-card>
</template>

<script>
import axios from 'axios'

export default {
    name: 'CrawlerManage',
    data() {
        return {
            form: {
                Wbtime: 10,
                Bdtime: 10,
                Bltime: 10
            }
        }
    },
    mounted() {
        this.getCrawlTime()
    },
    methods: {
        async getCrawlTime() {
            const username = localStorage.getItem('username')
            try{
                const res = await axios.get('http://127.0.0.1:8000/api/crawltime',{
                    params: {
                        username
                    }
                });
                this.form.Wbtime = res.data.Wbtime;
                this.form.Bdtime = res.data.Bdtime;
                this.form.Bltime = res.data.Bltime;
            } catch(error) {
                if (error.response) {
                    this.$message.error(error.response.data.detail);
                } else {
                    this.$message.error('网络请求失败！');
                }
            }
        },
        async updateCrawlTime() {
            try {
                const username = localStorage.getItem('username')
                const res = await axios.post('http://127.0.0.1:8000/api/updatecrawltime', {
                    username,
                    Wbtime: this.form.Wbtime,
                    Bdtime: this.form.Bdtime,
                    Bltime: this.form.Bltime
                });
                this.getCrawlTime();
                this.$message.success(res.data.message);
            } catch (error) {
                if (error.response) {
                    this.$message.error(error.response.data.detail);
                } else {
                    this.$message.error('网络请求失败！');
                }
            }
        }
    }
}
</script>