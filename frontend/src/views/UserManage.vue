<template>
    <div class="usermanage-container">
        <el-table
          :data="userList"
          border
          stripe
          style="width: 100%"
        >
            <el-table-column
                prop="id"
                label="用户编号"
                min-width="15%"
                align="center"
            />
            <el-table-column
                prop="username"
                label="用户名"
                min-width="15%"
                align="center"
            />
            <el-table-column
                prop="is_active"
                label="账号状态"
                min-width="15%"
                align="center"
            />
            <el-table-column
                prop="is_superuser"
                label="管理员"
                min-width="15%"
                align="center"
            />
            <el-table-column
                fixed="right"
                label="账号操作"
                align="center"
                min-width="55%"
            >
                <template #default="scope">
                    <el-button type="success" @click="activateUser(scope.row.username)">
                        启用用户
                    </el-button>
                    <el-button type="warning" @click="deactivateUser(scope.row.username)">
                        禁用用户
                    </el-button>
                    <el-button type="primary" @click="resetPassword(scope.row.username)">
                        重置密码
                    </el-button>
                    <el-button type="danger" @click="deleteUser(scope.row.username)">
                        删除用户
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>
  
<script>
import axios from 'axios';

export default {
  data() {
    return {
      userList: [],
    };
  },
  mounted() {
    this.fetchUserList();
  },
  methods: {
    async fetchUserList() {
      try {
        const username = localStorage.getItem('username');
        const response = await axios.get('http://127.0.0.1:8000/api/userlist', {
          params: { username }
        });
        response.data.forEach((user) => {
            user.is_superuser = user.is_superuser ? '是' : '否';
            user.is_active = user.is_active ? '已启用' : '已禁用';
        });
        this.userList = response.data;

      } catch (error) {
        if (error.response) {
            this.$message.error(
              error.response.data.detail
            );
        } else {
            this.$message.error('网络请求失败');
        }
      }
    },
    async activateUser(username) {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/activateuser', {
          params: { username }
        });
        this.$message.success(response.data.message);
        this.fetchUserList();
      } catch (error) {
        if (error.response) {
            this.$message.error(
              error.response.data.detail
            );
        } else {
              this.$message.error('网络请求失败');
        }
      }
    },
    async deactivateUser(username) {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/deactivateuser', {
          params: { username }
        });
        this.$message.success(response.data.message);
        this.fetchUserList();
      } catch (error) {
        if (error.response) {
            this.$message.error(
                error.response.data.detail
            );
        } else {
            this.$message.error('网络请求失败');
        }
      }
    },
    async deleteUser(username) {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/deleteuser', {
          params: { username }
        });
        this.$message.success(response.data.message);
        this.fetchUserList();
      } catch (error) {
        if (error.response) {
              this.$message.error(
                error.response.data.detail
              );
        } else {
            this.$message.error('网络请求失败');
        }
      }
    },
    async resetPassword(username) {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/resetpassword', {
          params: { username }
        });
        this.$message.success(response.data.message);
        this.fetchUserList();
      } catch (error) {
        if (error.response) {
            this.$message.error(
              error.response.data.detail
            )
        } else {
            this.$message.error('网络请求失败')
        }
      }
    }
  }
}
</script>