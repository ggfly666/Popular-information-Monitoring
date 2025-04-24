<template>
    <el-card style="max-width: 600px; margin-top: 50px;">
        <template #header>
            <div class="card-header">
                <span>热门分析推送管理</span>
            </div>
        </template>
        <el-form :model="form" label-width="auto" style="max-width: 600px">
            <el-form-item label="微博热门推送频率/h">
                <el-input-number v-model="form.Wbtime" :min="1" />
            </el-form-item>
            <el-form-item label="百度热门推送频率/h">
                <el-input-number v-model="form.Bdtime" :min="1" />
            </el-form-item>
            <el-form-item label="B站热门推送频率/h">
                <el-input-number v-model="form.Bltime" :min="1" />
            </el-form-item>
        </el-form>
        <template #footer>
            <div style="text-align: center;">
                <el-button type="primary" @click="getPushTime">刷新时间</el-button>
                <el-button type="primary" @click="updatePushTime">修改时间</el-button>
            </div>
        </template>
    </el-card>
</template>

<script>
import axios from 'axios'

export default {
    name: 'push',
    data() {
        return {
            form: {
                Wbtime: 10,
                Bdtime: 10,
                Bltime: 10
            },
            lastWbRequestTime: null,
            isWbRequesting: false,
            lastBdRequestTime: null,
            isBdRequesting: false,
            lastBlRequestTime: null,
            isBlRequesting: false
        };
    },
    mounted() {
        this.getPushTime();
        this.startWbInterval();
        this.startBdInterval();
        this.startBlInterval();
    },
    beforeDestroy() {
        this.stopWbInterval();
        this.stopBdInterval();
        this.stopBlInterval();
    },
    methods: {
        async getPushTime() {
            const username = localStorage.getItem('username')
            try{
                const res = await axios.get('http://127.0.0.1:8000/api/pushtime',{
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
        async updatePushTime() {
            try {
                const username = localStorage.getItem('username')
                const res = await axios.post('http://127.0.0.1:8000/api/updatepushtime', {
                    username,
                    Wbtime: this.form.Wbtime,
                    Bdtime: this.form.Bdtime,
                    Bltime: this.form.Bltime
                });
                this.getPushTime();
                this.$message.success(res.data.message);
            } catch (error) {
                if (error.response) {
                    this.$message.error(error.response.data.detail);
                } else {
                    this.$message.error('网络请求失败！');
                }
            }
        },
        async wbPush(){ 
            if (this.isWbRequesting) return;
            this.isWbRequesting = true;
            try {
                const now = Date.now();
                const interval = this.form.Wbtime * 3600 * 1000;
                if (this.lastWbRequestTime && (now - this.lastWbRequestTime < interval)) {
                    this.isWbRequesting = false; 
                    return;
                }
                const username = localStorage.getItem('username')
                const res = await axios.get('http://127.0.0.1:8000/api/wbhotsentiment/push',{
                    params: {
                        username
                    }
                });
                this.lastWbRequestTime = now;
                this.$message.success(res.data.message);
            } catch (error) {
                if (error.response) {
                    this.$message.error(error.response.data.detail);
                } else {
                    this.$message.error('网络请求失败！');
                }
            } finally {
                this.isWbRequesting = false;
            }
        },
        async startWbInterval() {
            const interval = this.form.Wbtime * 3600 * 1000;
            this.wbInterval = setInterval(() => this.wbPush(), interval); 
        },
        async stopWbInterval() {
            clearInterval(this.wbInterval);
        },
        async bdPush(){
            if (this.isBdRequesting) return;
            this.isBdRequesting = true;
            try {
                const now = Date.now();
                const interval = this.form.Bdtime * 3600 * 1000;
                if (this.lastBdRequestTime && (now - this.lastBdRequestTime < interval)) {
                    this.isBdRequesting = false; 
                    return;
                }
                const username = localStorage.getItem('username')
                const res = await axios.get('http://127.0.0.1:8000/api/bdhotsentiment/push',{
                    params: {
                        username
                    }
                });
                this.lastBdRequestTime = now;
                this.$message.success(res.data.message);
            } catch (error) {
                if (error.response) {
                    this.$message.error(error.response.data.detail);
                } else {
                    this.$message.error('网络请求失败！');
                }
            } finally {
                this.isBdRequesting = false;
            }
        },
        async startBdInterval() {
            const interval = this.form.Bdtime * 3600 * 1000;
            this.bdInterval = setInterval((() => this.bdPush(), interval));
        },
        async stopBdInterval() {
            clearInterval(this.bdInterval);
        },
        async blPush(){
            if (this.isBlRequesting) return;
            this.isBlRequesting = true;
            try {
                const now = Date.now();
                const interval = this.form.Bltime * 3600 * 1000;
                if (this.lastBlRequestTime && (now - this.lastBlRequestTime < interval)) {
                    this.isBlRequesting = false; 
                    return;
                }
                const username = localStorage.getItem('username')
                const res = await axios.get('http://127.0.0.1:8000/api/blhotsentiment/push',{
                    params: {
                        username
                    }
                });
                this.lastBltRequestTime = now;
                this.$message.success(res.data.message);
            } catch (error) {
                if (error.response) {
                    this.$message.error(error.response.data.detail);
                } else {
                    this.$message.error('网络请求失败！');
                }
            } finally {
                this.isBlRequesting = false;
            }
        },
        async startBlInterval() {
            const interval = this.form.Bltime * 3600 * 1000;
            this.blInterval = setInterval(() => this.blPush(), interval);
        },
        async stopBlInterval() {
            clearInterval(this.blInterval);
        }
    },
    watch: {
        'form.Wbtime': function () {
            this.stopWbInterval();
            this.startWbInterval();
        },
        'form.Bdtime': function () {
            this.stopBdInterval();
            this.startBdInterval();
        },
        'form.Bltime': function () {
            this.stopBlInterval();
            this.startBlInterval();
        }
    }
};
</script>