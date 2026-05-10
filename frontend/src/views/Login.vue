<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const activeTab = ref('login')
const loading = ref(false)

const loginForm = reactive({ username: '', password: '' })
const registerForm = reactive({ username: '', email: '', password: '', confirmPassword: '', invitationCode: '' })

const loginRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

const registerRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }, { min: 3, message: '至少3个字符', trigger: 'blur' }],
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }, { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }, { min: 3, message: '至少3个字符', trigger: 'blur' }],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: (rule, value, cb) => value === registerForm.password ? cb() : cb(new Error('两次密码不一致')), trigger: 'blur' },
  ],
  invitationCode: [{ required: true, message: '请输入邀请码', trigger: 'blur' }],
}

const loginFormRef = ref(null)
const registerFormRef = ref(null)

async function handleLogin() {
  const valid = await loginFormRef.value.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    await auth.login({ username: loginForm.username, password: loginForm.password })
    ElMessage.success('登录成功')
    router.push('/dashboard')
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '用户名或密码错误')
  } finally { loading.value = false }
}

async function handleRegister() {
  const valid = await registerFormRef.value.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    await auth.register({
      username: registerForm.username,
      email: registerForm.email,
      password: registerForm.password,
      password2: registerForm.confirmPassword,
      invitation_code: registerForm.invitationCode,
    })
    ElMessage.success('注册成功')
    router.push('/dashboard')
  } catch (err) {
    const msg = err.response?.data
    const detail = msg?.password?.[0] || msg?.username?.[0] || msg?.email?.[0] || msg?.detail || '注册失败，请重试'
    ElMessage.error(detail)
  } finally { loading.value = false }
}
</script>

<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-brand">
        <span class="login-icon">👶</span>
        <h1 class="login-title">宝宝博客</h1>
        <p class="login-subtitle">记录宝宝成长的每一个瞬间</p>
      </div>

      <div class="login-card card">
        <el-tabs v-model="activeTab" :stretch="true">
          <el-tab-pane label="登录" name="login">
            <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" @keyup.enter="handleLogin">
              <el-form-item prop="username">
                <el-input v-model="loginForm.username" placeholder="用户名" :prefix-icon="'User'" />
              </el-form-item>
              <el-form-item prop="password">
                <el-input v-model="loginForm.password" type="password" placeholder="密码" :prefix-icon="'Lock'" show-password />
              </el-form-item>
              <el-button type="primary" size="large" :loading="loading" @click="handleLogin" class="submit-btn">
                登录
              </el-button>
            </el-form>
          </el-tab-pane>

          <el-tab-pane label="注册" name="register">
            <el-form ref="registerFormRef" :model="registerForm" :rules="registerRules" @keyup.enter="handleRegister">
              <el-form-item prop="username">
                <el-input v-model="registerForm.username" placeholder="用户名" :prefix-icon="'User'" />
              </el-form-item>
              <el-form-item prop="email">
                <el-input v-model="registerForm.email" placeholder="邮箱" :prefix-icon="'Message'" />
              </el-form-item>
              <el-form-item prop="password">
                <el-input v-model="registerForm.password" type="password" placeholder="密码" :prefix-icon="'Lock'" show-password />
              </el-form-item>
              <el-form-item prop="confirmPassword">
                <el-input v-model="registerForm.confirmPassword" type="password" placeholder="确认密码" :prefix-icon="'Lock'" show-password />
              </el-form-item>
              <el-form-item prop="invitationCode">
                <el-input v-model="registerForm.invitationCode" placeholder="邀请码" :prefix-icon="'Key'" />
              </el-form-item>
              <el-button type="primary" size="large" :loading="loading" @click="handleRegister" class="submit-btn">
                注册
              </el-button>
            </el-form>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fef2f2 0%, #f0f9ff 50%, #f5f3ff 100%);
  padding: var(--space-4);
}

.login-container {
  width: 100%;
  max-width: 400px;
}

.login-brand {
  text-align: center;
  margin-bottom: var(--space-8);
}

.login-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: var(--space-3);
}

.login-title {
  font-size: var(--font-3xl);
  font-weight: 700;
  color: var(--color-primary);
  margin: 0 0 var(--space-2);
}

.login-subtitle {
  font-size: var(--font-sm);
  color: var(--color-text-muted);
  margin: 0;
}

.login-card {
  padding: var(--space-6);
  border-radius: var(--radius-lg);
}

.submit-btn {
  width: 100%;
  margin-top: var(--space-2);
}
</style>
