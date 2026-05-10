<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { uploadAvatar } from '@/api'

const emit = defineEmits(['selected'])

const loading = ref(false)

const avatars = [
  // 原有头像
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
  // 新增卡通头像
  { seed: 'cartoon-kitty', label: '卡通猫咪', style: 'fun-emoji' },
  { seed: 'cartoon-puppy', label: '卡通小狗', style: 'fun-emoji' },
  { seed: 'cartoon-bunny', label: '卡通兔兔', style: 'fun-emoji' },
  { seed: 'cartoon-bear', label: '卡通小熊', style: 'fun-emoji' },
  { seed: 'cartoon-fox', label: '卡通狐狸', style: 'fun-emoji' },
  { seed: 'cartoon-deer', label: '卡通小鹿', style: 'fun-emoji' },
  { seed: 'cartoon-penguin', label: '卡通企鹅', style: 'fun-emoji' },
  { seed: 'cartoon-duck', label: '卡通小鸭', style: 'fun-emoji' },
  { seed: 'cartoon-owl', label: '卡通猫头鹰', style: 'fun-emoji' },
  { seed: 'cartoon-panda', label: '国宝熊猫', style: 'fun-emoji' },
  { seed: 'cartoon-tiger', label: '卡通老虎', style: 'fun-emoji' },
  { seed: 'cartoon-lion', label: '卡通狮子', style: 'fun-emoji' },
  { seed: 'cartoon-elephant', label: '卡通大象', style: 'fun-emoji' },
  { seed: 'cartoon-monkey', label: '卡通猴子', style: 'fun-emoji' },
  { seed: 'cartoon-frog', label: '卡通青蛙', style: 'fun-emoji' },
  { seed: 'cartoon-whale', label: '卡通鲸鱼', style: 'fun-emoji' },
  { seed: 'cartoon-dolphin', label: '卡通海豚', style: 'fun-emoji' },
  { seed: 'cartoon-turtle', label: '卡通乌龟', style: 'fun-emoji' },
  { seed: 'cartoon-butterfly', label: '卡通蝴蝶', style: 'fun-emoji' },
  { seed: 'cartoon-sunflower', label: '卡通向日葵', style: 'fun-emoji' },
  { seed: 'cartoon-rainbow', label: '卡通彩虹', style: 'fun-emoji' },
  { seed: 'cartoon-star', label: '卡通星星', style: 'fun-emoji' },
  { seed: 'cartoon-moon', label: '卡通月亮', style: 'fun-emoji' },
  { seed: 'cartoon-crown', label: '卡通皇冠', style: 'fun-emoji' },
  { seed: 'cartoon-cake', label: '卡通蛋糕', style: 'fun-emoji' },
  { seed: 'cartoon-candy', label: '卡通糖果', style: 'fun-emoji' },
  { seed: 'cartoon-balloon', label: '卡通气球', style: 'fun-emoji' },
  { seed: 'cartoon-gift', label: '卡通礼物', style: 'fun-emoji' },
]

function getUrl(av) {
  const style = av.style || 'thumbs'
  return `https://api.dicebear.com/9.x/${style}/svg?seed=${av.seed}&backgroundColor_transparent=true`
}

async function select(av) {
  loading.value = true
  try {
    const resp = await fetch(getUrl(av))
    const blob = await resp.blob()
    const file = new File([blob], `${av.seed}.svg`, { type: 'image/svg+xml' })
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
        @click="select(av)"
        :title="av.label"
        :aria-label="`选择 ${av.label} 头像`"
      >
        <img :src="getUrl(av)" :alt="av.label" class="avatar-img" />
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
