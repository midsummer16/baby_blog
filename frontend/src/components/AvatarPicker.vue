<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { uploadAvatar } from '@/api'

const emit = defineEmits(['selected'])

const loading = ref(false)

const avatars = [
  { seed: 'baby1', label: '笑脸' },
  { seed: 'baby2', label: '星星' },
  { seed: 'baby3', label: '太阳' },
  { seed: 'baby4', label: '花朵' },
  { seed: 'baby5', label: '月亮' },
  { seed: 'baby6', label: '爱心' },
  { seed: 'bear1', label: '小熊' },
  { seed: 'bear2', label: '小兔' },
  { seed: 'cat1', label: '小猫' },
  { seed: 'cat2', label: '小狗' },
  { seed: 'frog1', label: '青蛙' },
  { seed: 'panda1', label: '熊猫' },
]

function getUrl(seed) {
  return `https://api.dicebear.com/9.x/thumbs/svg?seed=${seed}&backgroundColor_transparent=true`
}

async function select(seed) {
  loading.value = true
  try {
    const resp = await fetch(getUrl(seed))
    const blob = await resp.blob()
    const file = new File([blob], `${seed}.svg`, { type: 'image/svg+xml' })
    const formData = new FormData()
    formData.append('avatar', file)
    await uploadAvatar(formData)
    ElMessage.success('头像已更新')
    emit('selected')
  } catch {
    ElMessage.error('头像更新失败')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="avatar-picker" v-loading="loading">
    <div class="avatar-grid">
      <button
        v-for="av in avatars"
        :key="av.seed"
        class="avatar-option"
        @click="select(av.seed)"
        :title="av.label"
        :aria-label="`选择 ${av.label} 头像`"
      >
        <img :src="getUrl(av.seed)" :alt="av.label" class="avatar-img" />
      </button>
    </div>
  </div>
</template>

<style scoped>
.avatar-picker {
  min-height: 100px;
}

.avatar-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-2);
  padding: var(--space-2) 0;
}

.avatar-option {
  border: 2px solid var(--color-border, #e8eaed);
  border-radius: var(--radius-md, 10px);
  padding: var(--space-2);
  cursor: pointer;
  background: var(--color-surface, #fff);
  transition: all 0.15s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-option:hover {
  border-color: var(--color-primary, #409eff);
  background: var(--color-primary-light, #ecf5ff);
  transform: scale(1.05);
}

.avatar-option:focus-visible {
  outline: 2px solid var(--color-primary, #409eff);
  outline-offset: 2px;
}

.avatar-img {
  width: 48px;
  height: 48px;
  object-fit: contain;
}

@media (max-width: 480px) {
  .avatar-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
