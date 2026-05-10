<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getMilestones, createMilestone } from '@/api'
import NavBar from '@/components/NavBar.vue'

const router = useRouter()

const milestones = ref([])
const loading = ref(true)
const dialogVisible = ref(false)
const submitting = ref(false)

const milestoneIcons = {
  birth: '👶', first_smile: '😊', roll_over: '🔄', sit: '🪑',
  crawl: '🧸', stand: '🧍', walk: '👣', first_word: '👶',
  speak: '🗣️', tooth: '🦷', first_bite: '🥄', wean: '🍼',
  first_step: '👟', run: '🏃', clap: '👏', wave: '👋',
  first_drawing: '🎨', potty_train: '🚽', kindergarten: '🎒',
  first_tooth_lost: '🦷', ride_bike: '🚲', swim: '🏊', read: '📖',
  other: '⭐',
}

const milestoneLabels = {
  birth: '出生', first_smile: '第一次微笑', roll_over: '翻身', sit: '坐',
  crawl: '爬', stand: '站立', walk: '走路', first_word: '叫妈妈/爸爸',
  speak: '说话', tooth: '长牙', first_bite: '第一次吃辅食', wean: '断奶',
  first_step: '独立行走', run: '跑步', clap: '拍手', wave: '挥手再见',
  first_drawing: '第一幅画', potty_train: '如厕训练', kindergarten: '上幼儿园',
  first_tooth_lost: '换牙', ride_bike: '骑自行车', swim: '游泳', read: '自己看书',
  other: '其他',
}

const milestoneTypes = Object.entries(milestoneIcons).map(([value, icon]) => ({
  value, label: `${icon} ${milestoneLabels[value]}`,
}))

const newMilestone = ref({ milestone_type: '', date: '', description: '' })

const sortedMilestones = computed(() => {
  const map = new Map()
  for (const ms of milestones.value) {
    const key = `${ms.milestone_type}_${ms.achieved_date}`
    if (!map.has(key) || (ms.post && !map.get(key).post)) {
      map.set(key, ms)
    }
  }
  return [...map.values()].sort((a, b) => new Date(b.achieved_date) - new Date(a.achieved_date))
})

async function fetchMilestones() {
  loading.value = true
  try {
    const res = await getMilestones()
    milestones.value = res.data.results ?? res.data
  } catch { ElMessage.error('加载里程碑失败') }
  finally { loading.value = false }
}

function openDialog() {
  newMilestone.value = { milestone_type: '', date: '', description: '' }
  dialogVisible.value = true
}

async function handleCreate() {
  if (!newMilestone.value.milestone_type || !newMilestone.value.date) {
    return ElMessage.warning('请选择里程碑类型和日期')
  }
  submitting.value = true
  try {
    await createMilestone({
      milestone_type: newMilestone.value.milestone_type,
      achieved_date: newMilestone.value.date,
      description: newMilestone.value.description,
    })
    ElMessage.success('里程碑创建成功')
    dialogVisible.value = false
    fetchMilestones()
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '创建失败')
  } finally { submitting.value = false }
}

function goToPost(postId) {
  if (postId) router.push(`/post/${postId}`)
}

onMounted(() => { fetchMilestones() })
</script>

<template>
  <div class="milestones-page">
    <NavBar />
    <main class="page-container">
      <div class="page-header">
        <h1 class="page-title">🏆 成长里程碑</h1>
        <el-button type="primary" @click="openDialog">
          <el-icon><Plus /></el-icon>添加里程碑
        </el-button>
      </div>

      <div v-if="loading" class="skeleton-grid">
        <div v-for="i in 4" :key="i" class="skeleton-card card">
          <div class="skeleton skeleton-icon" />
          <div class="skeleton skeleton-line w-1/2" style="margin:12px auto" />
          <div class="skeleton skeleton-line w-1/3" style="margin:0 auto" />
        </div>
      </div>

      <div v-else-if="!sortedMilestones.length" class="empty-state">
        <div class="empty-state-icon">🏆</div>
        <h3>还没有里程碑记录</h3>
        <p>开始记录宝宝的每个重要成长时刻吧</p>
        <el-button type="primary" @click="openDialog">添加第一个里程碑</el-button>
      </div>

      <template v-else>
        <div class="milestone-grid">
          <div
            v-for="ms in sortedMilestones"
            :key="ms.id"
            class="milestone-card card"
            @click="ms.post ? goToPost(ms.post) : null"
            :class="{ clickable: !!ms.post }"
          >
            <div class="milestone-icon">{{ milestoneIcons[ms.milestone_type] || '⭐' }}</div>
            <div class="milestone-type">{{ milestoneLabels[ms.milestone_type] || ms.milestone_type }}</div>
            <div class="milestone-date">{{ ms.achieved_date }}</div>
            <p v-if="ms.description" class="milestone-desc">{{ ms.description }}</p>
          </div>
        </div>
      </template>
    </main>

    <el-dialog v-model="dialogVisible" title="添加里程碑" width="90%" max-width="480px">
      <el-form label-position="top">
        <el-form-item label="里程碑类型">
          <el-select v-model="newMilestone.milestone_type" placeholder="选择类型" class="full-width">
            <el-option v-for="mt in milestoneTypes" :key="mt.value" :label="mt.label" :value="mt.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="日期">
          <el-date-picker v-model="newMilestone.date" type="date" placeholder="选择日期" format="YYYY-MM-DD" value-format="YYYY-MM-DD" class="full-width" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="newMilestone.description" type="textarea" :rows="3" placeholder="简单描述这个里程碑..." />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleCreate">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.milestones-page { min-height: 100vh; background: var(--color-bg); }

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-6);
  flex-wrap: wrap;
  gap: var(--space-3);
}

.page-title { margin: 0; }

/* Skeleton */
.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-4);
}

.skeleton-card { padding: var(--space-6); text-align: center; }
.skeleton-icon { width: 48px; height: 48px; border-radius: 50%; margin: 0 auto var(--space-4); }
.w-1\2 { width: 50%; }
.w-1\3 { width: 33%; }

/* Milestone grid */
.milestone-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-4);
}

.milestone-card {
  text-align: center;
  padding: var(--space-6) var(--space-4);
  transition: transform 0.15s;
}

.milestone-card:hover { transform: translateY(-2px); }
.milestone-card.clickable { cursor: pointer; }

.milestone-icon { font-size: 2.5rem; margin-bottom: var(--space-3); line-height: 1; }
.milestone-type { font-weight: 600; font-size: var(--font-lg); color: var(--color-text); margin-bottom: var(--space-1); }
.milestone-date { font-size: var(--font-sm); color: var(--color-text-muted); }
.milestone-desc { margin: var(--space-2) 0 0; font-size: var(--font-sm); color: var(--color-text-secondary); }

.full-width { width: 100%; }

@media (max-width: 768px) {
  .milestone-grid { grid-template-columns: 1fr; }
  .skeleton-grid { grid-template-columns: 1fr; }
}
</style>
