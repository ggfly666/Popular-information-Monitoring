<template>
    <div class="common-layout">
      <el-container>
        <el-aside width="200px">
            <el-menu default-active="0" style="margin-top: 50px">
                <el-menu-item index="0">
                    <template #title>
                        <el-icon><HomeFilled /></el-icon>
                        <span style="width: 100%;"@click="$router.push('/sjdp')">数据大屏</span>
                    </template>
                </el-menu-item>
                <el-menu-item index="1">
                    <template #title>
                        <el-icon><List /></el-icon>
                        <span style="width: 100%;"@click="$router.push('/hotlist')">热门列表</span>
                    </template>
                </el-menu-item>
                <el-menu-item index="2">
                    <template #title>
                        <el-icon><TrendCharts /></el-icon>
                        <span style="width: 100%;"@click="$router.push('/hotanalysis')">情感分析</span>
                    </template>
                </el-menu-item>
                <el-menu-item index="3">
                    <template #title>
                        <el-icon><Share /></el-icon>
                        <span style="width: 100%;"@click="$router.push('/push')">推送管理</span>
                    </template>
                </el-menu-item>
                <el-menu-item index="4">
                    <template #title>
                        <el-icon><UserFilled /></el-icon>
                        <span style="width: 100%;"@click="$router.push('/userinfo')">个人信息</span>
                    </template>
                </el-menu-item>
                <el-menu-item index="5" v-if="is_superuser==='true'">
                    <template #title>
                        <el-icon><ChromeFilled /></el-icon>
                        <span style="width: 100%;"@click="$router.push('/crawlermanage')">爬虫管理</span>
                    </template>
                </el-menu-item>
                <el-menu-item index="6" v-if="is_superuser==='true'">
                    <template #title>
                        <el-icon><Avatar /></el-icon>
                        <span style="width: 100%;"@click="$router.push('/usermanage')">用户管理</span>
                    </template>
                </el-menu-item>
                <el-menu-item index="7" v-if="is_superuser==='true'">
                    <template #title>
                        <el-icon><Management /></el-icon>
                        <span style="width: 100%;"@click="$router.push('/systemlog')">系统日志</span>
                    </template>
                </el-menu-item>
                <el-menu-item index="8">
                    <template #title>
                        <el-icon><Promotion /></el-icon>
                        <span style="width: 100%;"@click="dialogVisible = true">退出登录</span>
                    </template>
                </el-menu-item>
            </el-menu>
            <el-dialog v-model="dialogVisible" title="退出登录" width="30%">
                <template #footer>
                    <el-button type="danger" @click="GotoLogout">确认</el-button>
                    <el-button type="primary" @click="dialogVisible = false">取消</el-button>
                </template>
            </el-dialog>
        </el-aside>
        <el-container>
          <el-main>
            <router-view></router-view>
          </el-main>
        </el-container>
      </el-container>
    </div>
</template>


<script>
export default {
    setup() {
        const username = localStorage.getItem('username') || ''
        const is_superuser = localStorage.getItem('is_superuser') || ''
        return {
            username,
            is_superuser
        }
    },
    data() {
        return {
            dialogVisible: false
        }
    },
    name: 'Home',
    methods: {
        async GotoLogout() {
            localStorage.removeItem('username')
            localStorage.removeItem('is_superuser')
            this.$message.success('退出登录成功！')
            this.$router.push({
                path: '/login'
            })
        },
    }
}
</script>

