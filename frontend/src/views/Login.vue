<template>
    <div class="login-container">
      <el-card class="box-card">
        <div slot="header" class="header">
          <h2>用户登录</h2>
        </div>
        <el-form :model="form" :rules="rules" ref="loginForm" label-width="70px" >
          <el-form-item label="用户名" prop="username">
            <el-input
              v-model="form.username"
              placeholder="请输入用户名"
              prefix-icon="el-icon-user"
            />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入密码"
              prefix-icon="el-icon-lock"
            />
          </el-form-item>
          <div class="button-group">
            <el-button
              type="primary"
              @click="submitForm('loginForm')"
              :loading="loading"
              style="width: 100%"
            >
              登录
            </el-button>
          </div>
          <div class="register-link">
            <el-link type="primary" :underline="false" href="/register" style="display: block;">
              还没有账号？去注册
            </el-link>
          </div>
          <div style="color: burlywood; font-size: 11px; text-align: center;">
            <span>若忘记密码，请联系管理员邮箱admin@admin.com。</span>
          </div>
          <div style="color: burlywood; font-size: 11px; text-align: center;">
            <span>若账号被禁用，请联系管理员邮箱admin@admin.com。</span>
          </div>
        </el-form>
      </el-card>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      },
      loading: false
    };
  },
  methods: {
    async submitForm(formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          this.loading = true;
          try {
            const res = await axios.post('http://127.0.0.1:8000/api/login', this.form);
            this.$message.success(res.data.message);
            localStorage.setItem('username', res.data.username);
            localStorage.setItem('is_superuser', res.data.is_superuser);
            this.$router.push({ path: '/' });
          } catch (error) {
            if (error.response) {
              this.$message.error(
                error.response.data.detail
              );
            } else {
              this.$message.error('网络请求失败');
            }
          }
          this.loading = false;
        }
      });
    }
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: #f0f2f5;
}

.box-card {
  width: 360px;
}

.header h2 {
  text-align: center;
  color: #409eff;
}

.el-form {
  padding: 0 20px;
}

.button-group {
  margin-top: 20px;
}

.register-link {
  margin-top: 15px;
  margin-bottom: 10px; 
  text-align: center;
}


.input-field .el-input__inner {
  width: 100%; 
  height: 40px; 
  padding: 0 35px; 
}


.el-form-item__label {
  padding: 0 12px 0 0; 
}
</style>