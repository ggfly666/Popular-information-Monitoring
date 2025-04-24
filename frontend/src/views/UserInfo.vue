<template>
    <el-descriptions
      :column="1" 
      title="用户信息"
      size="large"
      border
      label-width="200px"
    >
        <el-descriptions-item>
            <template #label>
                <el-icon color="#409efc">
                    <aim />
                </el-icon>
                用户编号
            </template>
            {{ userinfo.id }}
        </el-descriptions-item>
        <el-descriptions-item>
            <template #label>
                <el-icon color="#409efc">
                    <user />
                </el-icon>
                用户名
            </template>
            {{ userinfo.username }}
        </el-descriptions-item>
        <el-descriptions-item>
            <template #label>
                <el-icon color="#409efc">
                    <key />
                </el-icon>
                密码(已加密)
            </template>
            <div>
                <span v-if="showPassword">{{ userinfo.password }}</span>
                <span v-else >
                    <span v-for="n in userinfo.password?.length" :key="n">*</span>
                </span >
                <el-button 
                type="primary"
                link
                @click="showPassword = !showPassword" 
                style="margin-left: 20px;"
                >
                    <el-icon v-if="showPassword" :size="16">
                        <Hide />
                    </el-icon>
                    <el-icon v-else :size="16">
                        <View />
                    </el-icon>
                </el-button>
            </div>
        </el-descriptions-item>
        <el-descriptions-item>
            <template #label>
                <el-icon color="#409efc">
                    <message />
                </el-icon>
                邮箱
            </template>
            {{ userinfo.email }}
        </el-descriptions-item>
        <el-descriptions-item>
            <template #label>
                <el-icon color="#409efc">
                    <setting />
                </el-icon>
                账号状态
            </template>
            {{ userinfo.is_active ? '启用' : '禁用' }}
        </el-descriptions-item>
        <el-descriptions-item>
            <template #label>
                <el-icon color="#409efc">
                    <star />
                </el-icon>
                管理员状态
            </template>
            {{ userinfo.is_superuser ? '是' : '否' }}
        </el-descriptions-item>
    </el-descriptions>
    <div class="user-info-buttons">
        <h4>账号操作</h4>
        <el-button type="primary" @click="updateUsernameDialog = true">修改用户名</el-button>
        <el-button type="primary" @click="updatePasswordDialog = true">修改密码</el-button>
        <el-button type="primary" @click="updateEmailDialog = true">修改邮箱</el-button>
        <el-button type="danger" @click="deleteUserDialog = true">注销账号</el-button>
        <el-divider />
        <div style="color: #409efc; font-size: 12px;">
            <span>若想成为管理员用户，请联系管理员邮箱admin@admin.com。</span>
        </div>
    </div>
    <el-dialog 
        title="修改用户名" 
        v-model="updateUsernameDialog" 
        width="30%">
        <el-input 
            v-model="newUsername" 
            placeholder="请输入新用户名" 
            style="width: 80%;"></el-input>
        <template #footer>
            <el-button @click="updateUsernameDialog = false">取消</el-button>
            <el-button type="primary" @click="handleUpdateUsername">确认</el-button>
        </template>
    </el-dialog>
    <el-dialog 
        title="修改密码" 
        v-model="updatePasswordDialog" 
        width="30%">
        <el-input 
            v-model="newPassword" 
            placeholder="请输入新密码" 
            type="password" 
            style="width: 80%;"></el-input>
        <template #footer>
            <el-button @click="updatePasswordDialog = false">取消</el-button>
            <el-button type="primary" @click="handleUpdatePassword">确认</el-button>
        </template>
    </el-dialog>
    <el-dialog 
        title="修改邮箱" 
        v-model="updateEmailDialog" 
        width="30%">
        <el-input 
            v-model="newEmail" 
            placeholder="请输入新邮箱" 
            style="width: 80%;"></el-input>
        <template #footer>
            <el-button @click="updateEmailDialog = false">取消</el-button>
            <el-button type="primary" @click="handleUpdateEmail">确认</el-button>
        </template>
    </el-dialog>
    <el-dialog 
        title="注销账号" 
        v-model="deleteUserDialog" 
        width="30%">
        <p>确定要注销账号吗？</p>
        <template #footer>
            <el-button @click="deleteUserDialog = false">取消</el-button>
            <el-button type="danger" @click="handleDeleteUser">注销</el-button>
        </template>
    </el-dialog>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      userinfo: {},
      showPassword: false,  
      updateUsernameDialog: false,
      updatePasswordDialog: false,
      updateEmailDialog: false,
      deleteUserDialog: false,
      newUsername: '',
      newPassword: '',
      newEmail: '',
    };
  },
  mounted() {
    this.fetchUserInfo();
  },
  methods: {
    async fetchUserInfo() {
        const username = localStorage.getItem('username') || '';
        try {
            const response = await axios.get('http://127.0.0.1:8000/api/userinfo',{
                params: { username }
            });
        this.userinfo = response.data;
        }catch (error) {
            this.$message.error(
            error.response.data.detail
        );
      }
    },
    async handleUpdateUsername() {
        localStorage.setItem('username', this.newUsername);
        const payload = {
            username: this.userinfo.username,
            updateusername: this.newUsername,
            updatepassword: '',
            updateemail: ''
        };
        try {
            const res = await axios.post('http://127.0.0.1:8000/api/updateuser', payload);
            this.$message.success(res.data.message);
            this.updateUsernameDialog = false;
            this.fetchUserInfo();
            this.newUsername = ''; 
        } catch (error) {
            this.$message.error(error.response.data.detail);
        }
    },


    async handleUpdatePassword() {
        const payload = {
            username: this.userinfo.username,
            updatepassword: this.newPassword,
            updateusername: '',
            updateemail: ''
        };
        try {
            const res = await axios.post('http://127.0.0.1:8000/api/updateuser', payload);
            this.$message.success(res.data.message);
            this.updatePasswordDialog = false;
            this.newPassword = '';
        } catch (error) {
            this.$message.error(error.response.data.detail);
        }
    },


    async handleUpdateEmail() {
        const payload = {
            username: this.userinfo.username,
            updateemail: this.newEmail,
            updateusername: '',
            updatepassword: ''
        };
        try {
            const res = await axios.post('http://127.0.0.1:8000/api/updateuser', payload);
            this.$message.success(res.data.message);
            this.updateEmailDialog = false;
            this.fetchUserInfo();
            this.newEmail = '';
        } catch (error) {
            this.$message.error(error.res.data.detail);
        }
    },
    async handleDeleteUser() {
        try {
            const username = localStorage.getItem('username') || '';
            const response = await axios.get('http://127.0.0.1:8000/api/deleteuser', {
            params: { username }
            });
            this.$message.success(response.data.message);
            this.$router.push({
                path: '/login'
            })
        } catch (error) {
            this.$message.error(error.response.data.detail);
      }
    }
  }
}

</script>


<style scoped>
.user-info-buttons {
  margin-top: 10px;
}
</style>