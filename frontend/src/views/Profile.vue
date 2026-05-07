<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { changePassword } from '@/api'
import { useAuthStore } from '@/stores/auth'
import NavBar from '@/components/NavBar.vue'
import AvatarPicker from '@/components/AvatarPicker.vue'

const router = useRouter()
const auth = useAuthStore()

const loading = ref(false)
const avatarUploading = ref(false)
const avatarPickerVisible = ref(false)

const profileForm = reactive({
  email: '',
  bio: '',
  phone: '',
})

const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: '',
})

const profileRules = {
  email: [
    { type: 'email', message: '请输入有效邮箱', trigger: 'blur' },
  ],
}

onMounted(() => {
  if (auth.user) {
    profileForm.email = auth.user.email || ''
    profileForm.bio = auth.user.bio || ''
    profileForm.phone = auth.user.phone || ''
  }
})

async function handleAvatarUpload(uploadFile) {
  const file = uploadFile.raw
  if (!file.type.startsWith('image/')) {
    ElMessage.error('请上传图片文件')
    return false
  }
  avatarUploading.value = true
  try {
    await auth.uploadAvatar(file)
    ElMessage.success('头像更新成功')
  } catch {
    ElMessage.error('头像上传失败')
  } finally {
    avatarUploading.value = false
  }
  return false
}

async function handleSave() {
  loading.value = true
  try {
    await auth.updateProfile({
      email: profileForm.email,
      bio: profileForm.bio,
      phone: profileForm.phone,
    })
    ElMessage.success('保存成功')
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '保存失败')
  } finally {
    loading.value = false
  }
}

async function handleChangePassword() {
  if (!passwordForm.oldPassword || !passwordForm.newPassword) {
    ElMessage.warning('请填写旧密码和新密码')
    return
  }
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    ElMessage.warning('两次密码不一致')
    return
  }
  if (passwordForm.newPassword.length < 3) {
    ElMessage.warning('新密码至少3个字符')
    return
  }
  loading.value = true
  try {
    await changePassword({
      old_password: passwordForm.oldPassword,
      new_password: passwordForm.newPassword,
    })
    ElMessage.success('密码修改成功')
    passwordForm.oldPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '密码修改失败')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="profile-page">
    <NavBar />

    <div class="profile-content">
      <h2 class="page-title">👤 个人信息</h2>

      <el-card shadow="never" class="profile-card">
        <div class="avatar-section">
          <el-avatar :size="100" :src="auth.user?.avatar" class="profile-avatar" />
          <div class="avatar-actions">
            <el-upload
              action=""
              :show-file-list="false"
              :auto-upload="false"
              :on-change="handleAvatarUpload"
              accept="image/*"
            >
              <el-button :loading="avatarUploading" size="small">上传头像</el-button>
            </el-upload>
            <el-button size="small" @click="avatarPickerVisible = true">选择头像</el-button>
          </div>
        </div>

        <el-dialog v-model="avatarPickerVisible" title="选择头像" width="90%" max-width="420px">
          <AvatarPicker @selected="avatarPickerVisible = false" />
        </el-dialog>

        <el-form
          :model="profileForm"
          :rules="profileRules"
          label-position="top"
        >
          <el-form-item label="用户名">
            <el-input :model-value="auth.user?.username" disabled />
          </el-form-item>

          <el-form-item label="邮箱" prop="email">
            <el-input v-model="profileForm.email" placeholder="请输入邮箱" />
          </el-form-item>

          <el-form-item label="简介">
            <el-input
              v-model="profileForm.bio"
              type="textarea"
              :rows="3"
              placeholder="写一句介绍..."
            />
          </el-form-item>

          <el-form-item label="手机号">
            <el-input v-model="profileForm.phone" placeholder="请输入手机号" />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              :loading="loading"
              @click="handleSave"
            >保存修改</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <el-card shadow="never" class="password-card">
        <template #header>
          <span>🔒 修改密码</span>
        </template>

        <el-form :model="passwordForm" label-position="top">
          <el-form-item label="旧密码">
            <el-input
              v-model="passwordForm.oldPassword"
              type="password"
              placeholder="输入旧密码"
              show-password
            />
          </el-form-item>

          <el-form-item label="新密码">
            <el-input
              v-model="passwordForm.newPassword"
              type="password"
              placeholder="输入新密码（至少3个字符）"
              show-password
            />
          </el-form-item>

          <el-form-item label="确认新密码">
            <el-input
              v-model="passwordForm.confirmPassword"
              type="password"
              placeholder="再次输入新密码"
              show-password
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="warning"
              :loading="loading"
              @click="handleChangePassword"
            >修改密码</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding-top: 60px;
}
.profile-content {
  max-width: 600px;
  margin: 0 auto;
  padding: 24px 16px;
}
.page-title {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 24px;
  color: #303133;
}
.profile-card,
.password-card {
  border-radius: 12px;
  padding: 8px;
  margin-bottom: 24px;
}
.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid #f0f0f0;
}
.profile-avatar {
  border: 3px solid #ecf5ff;
}
.avatar-actions {
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
  justify-content: center;
}
</style>
