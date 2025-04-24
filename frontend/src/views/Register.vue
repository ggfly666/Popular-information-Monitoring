<template>
    <div class="register-container">
      <el-card class="box-card">
        <div slot="header" class="header">
          <h2>用户注册</h2>
        </div>
        <el-form :model="form" :rules="rules" ref="registerForm" label-width="80px">
          <!-- 用户名输入 -->
          <el-form-item label="用户名" prop="username">
            <el-input
              v-model="form.username"
              placeholder="请输入用户名"
              prefix-icon="el-icon-user"
            />
          </el-form-item>
  
          <!-- 邮箱输入 -->
          <el-form-item label="邮箱" prop="email">
            <el-input
              v-model="form.email"
              placeholder="请输入邮箱地址"
              prefix-icon="el-icon-message"
            />
          </el-form-item>
  
          <!-- 密码输入 -->
          <el-form-item label="密码" prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入密码"
              prefix-icon="el-icon-lock"
            />
          </el-form-item>
  
          <!-- 确认密码输入 -->
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input
              v-model="form.confirmPassword"
              type="password"
              placeholder="请再次输入密码"
              prefix-icon="el-icon-lock"
            />
          </el-form-item>
  
          <!-- 注册按钮 -->
          <div class="button-group">
            <el-button
              type="primary"
              @click="submitForm('registerForm')"
              :loading="loading"
              style="width: 100%"
            >
              注册
            </el-button>
          </div>
          <div class="login-link">
            <el-link type="primary" :underline="false" href="/login" style="display: block;">
              已有账号？去登录
            </el-link>
          </div>
        </el-form>
      </el-card>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      const validateConfirmPassword = (rule, value, callback) => {
        if (value !== this.form.password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      }
      return {
        form: {
          username: '',
          email: '',
          password: '',
          confirmPassword: ''
        },
        rules: {
          username: [
            { required: true, message: '请输入用户名', trigger: 'blur' }
          ],
          email: [
            { required: true, message: '请输入邮箱', trigger: 'blur' },
            { type: 'email', message: '请输入有效邮箱', trigger: 'blur' }
          ],
          password: [
            { required: true, message: '请输入密码', trigger: 'blur' }
          ],
          confirmPassword: [
            { required: true, message: '请确认密码', trigger: 'blur' },
            { validator: validateConfirmPassword, trigger: 'blur' }
          ]
        },
        loading: false
      }
    },
    methods: {
      async submitForm(formName) {
        this.$refs[formName].validate(async valid => {
          if (valid) {
            this.loading = true
            try {
              const res = await axios.post('http://127.0.0.1:8000/api/register', {
                username: this.form.username,
                password: this.form.password,
                email: this.form.email
              })
              this.$message.success(res.data.message)
              this.$router.push({ path: '/login' })
            } catch (error) {
              if (error.response) {
                this.$message.error(error.response.data.detail)
              } else {
                this.$message.error('网络请求失败')
              }
            }
            this.loading = false
          }
        })
      }
    }
  }
  </script>
  
  <style scoped>
  .register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: #f0f2f5;
  }
  
  .box-card {
    width: 420px;
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

  .login-link {
  margin-top: 15px; 
  text-align: center; 
}
  </style>