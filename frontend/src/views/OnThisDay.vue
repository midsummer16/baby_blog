<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getOnThisDay } from '@/api'
import PostCard from '@/components/PostCard.vue'
import NavBar from '@/components/NavBar.vue'

const loading = ref(false)
const lastYearPosts = ref([])
const lastMonthPosts = ref([])

async function fetchData() {
  loading.value = true
  try {
    const res = await getOnThisDay()
    const data = res.data
    lastYearPosts.value = data.last_year ?? data.last_year_posts ?? []
    lastMonthPosts.value = data.last_month ?? data.last_month_posts ?? []
  } catch {
    ElMessage.error('获取历史数据失败')
  } finally {
    loading.value = false
  }
}

function refreshPosts() {
  // no-op
}

onMounted(() => {
  fetchData()
})
</script>

<template>
  <div class="on-this-day-page">
    <NavBar />

    <div class="otd-content">
      <h2 class="page-title">📅 历史上的今天</h2>

      <div v-loading="loading" class="otd-sections">
        <section class="otd-section">
          <div class="section-header">
            <el-icon :size="24"><Timer /></el-icon>
            <h3>去年今日 ({{ lastYearPosts.length }})</h3>
          </div>

          <div v-if="lastYearPosts.length" class="post-list">
            <PostCard
              v-for="post in lastYearPosts"
              :key="post.id"
              :post="post"
              @refresh="refreshPosts"
            />
          </div>
          <el-empty v-else description="去年今日暂无记录" />
        </section>

        <el-divider />

        <section class="otd-section">
          <div class="section-header">
            <el-icon :size="24"><Clock /></el-icon>
            <h3>上月同日 ({{ lastMonthPosts.length }})</h3>
          </div>

          <div v-if="lastMonthPosts.length" class="post-list">
            <PostCard
              v-for="post in lastMonthPosts"
              :key="post.id"
              :post="post"
              @refresh="refreshPosts"
            />
          </div>
          <el-empty v-else description="上月同日暂无记录" />
        </section>
      </div>
    </div>
  </div>
</template>

<style scoped>
.on-this-day-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding-top: 60px;
}
.otd-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px 16px;
}
.page-title {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 24px;
  color: #303133;
}
.otd-sections {
  min-height: 200px;
}
.otd-section {
  margin-bottom: 16px;
}
.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}
.section-header h3 {
  margin: 0;
  font-size: 20px;
  color: #303133;
}
.post-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
</style>
