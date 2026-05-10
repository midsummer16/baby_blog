<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUsers, adminResetPassword } from '@/api'
import { useAuthStore } from '@/stores/auth'
import NavBar from '@/components/NavBar.vue'

const auth = useAuthStore()
const users = ref([])
const loading = ref(true)
const dialogVisible = ref(false)
const resetForm = ref({ userId: null, username: '', newPassword: '' })
const submitting = ref(false)

async function fetchUsers() {
  loading.value = true
  try {
    const res = await getUsers()
    users.value = res.data.results ?? res.data
  } catch {
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

function openResetDialog(user) {
  resetForm.value = { userId: user.id, username: user.username, newPassword: '' }
  dialogVisible.value = true
}

async function handleReset() {
  if (!resetForm.value.newPassword.trim()) {
    return ElMessage.warning('请输入新密码')
  }
  if (resetForm.value.newPassword.length < 3) {
    return ElMessage.warning('密码至少3个字符')
  }
  submitting.value = true
  try {
    await adminResetPassword(resetForm.value.userId, {
      new_password: resetForm.value.newPassword,
    })
    ElMessage.success(`已重置用户 ${resetForm.value.username} 的密码`)
    dialogVisible.value = false
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '操作失败')
  } finally {
    submitting.value = false
  }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

onMounted(() => {
  fetchUsers()
})
</script>

<template>
  <div class="user-manage-page">
    <NavBar />
    <main class="page-container">
      <div class="page-header">
        <h1 class="page-title">👥 用户管理</h1>
        <el-tag type="danger" size="large">管理员</el-tag>
      </div>

      <el-card shadow="never" class="user-table-card">
        <div v-loading="loading">
          <el-table :data="users" stripe style="width: 100%" empty-text="暂无用户">
            <el-table-column prop="id" label="ID" width="60" />
            <el-table-column label="头像" width="70">
              <template #default="{ row }">
                <el-avatar :size="36" :src="row.avatar" />
              </template>
            </el-table-column>
            <el-table-column prop="username" label="用户名" min-width="120" />
            <el-table-column prop="email" label="邮箱" min-width="160">
              <template #default="{ row }">
                {{ row.email || '-' }}
              </template>
            </el-table-column>
            <el-table-column label="角色" width="100">
              <template #default="{ row }">
                <el-tag :type="row.role === 'admin' ? 'danger' : 'info'" size="small">
                  {{ row.role === 'admin' ? '管理员' : '普通用户' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="注册时间" width="120">
              <template #default="{ row }">
                {{ formatDate(row.date_joined) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120" fixed="right">
              <template #default="{ row }">
                <el-button
                  type="warning"
                  size="small"
                  @click="openResetDialog(row)"
                >重置密码</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>
    </main>

    <el-dialog v-model="dialogVisible" title="重置用户密码" width="90%" max-width="420px">
      <el-form label-position="top">
        <el-form-item label="目标用户">
          <el-input :model-value="resetForm.username" disabled />
        </el-form-item>
        <el-form-item label="新密码">
          <el-input
            v-model="resetForm.newPassword"
            type="password"
            placeholder="请输入新密码（至少3个字符）"
            show-password
            @keyup.enter="handleReset"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="warning" :loading="submitting" @click="handleReset">确认重置</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.user-manage-page {
  min-height: 100vh;
  background: var(--color-bg);
}

.page-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-6);
}

.page-title {
  margin: 0;
}

.user-table-card {
  border-radius: var(--radius-md);
}

@media (max-width: 768px) {
  .user-table-card :deep(.el-table) {
    font-size: 13px;
  }
}
</style>
