<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getPosts, getUsers } from '@/api'
import PostCard from '@/components/PostCard.vue'
import NavBar from '@/components/NavBar.vue'

const router = useRouter()

const posts = ref([])
const users = ref([])
const selectedAuthor = ref('')
const loading = ref(true)
const page = ref(1)
const hasMore = ref(true)
const loadingMore = ref(false)

async function fetchUsers() {
  try {
    const res = await getUsers()
    users.value = res.data.results ?? res.data
  } catch { /* not critical */ }
}

async function fetchPosts() {
  loading.value = true
  try {
    const params = { page: page.value }
    if (selectedAuthor.value) params.author = selectedAuthor.value
    const res = await getPosts(params)
    const newPosts = res.data.results ?? res.data
    if (page.value === 1) posts.value = newPosts
    else posts.value = [...posts.value, ...newPosts]
    hasMore.value = newPosts.length >= 20
  } catch {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

function loadMore() {
  if (loadingMore.value || !hasMore.value) return
  loadingMore.value = true
  page.value++
  fetchPosts().finally(() => { loadingMore.value = false })
}

function handleFilter() {
  page.value = 1
  fetchPosts()
}

function goUpload() {
  router.push('/upload')
}

onMounted(() => {
  fetchUsers()
  fetchPosts()
})
</script>

<template>
  <div class="dashboard-page">
    <NavBar />
    <main class="page-container">
      <div class="dash-header">
        <h1 class="page-title">时光轴</h1>
        <el-select
          v-model="selectedAuthor"
          placeholder="全部作者"
          clearable
          size="small"
          @change="handleFilter"
          class="author-filter"
        >
          <el-option label="全部作者" value="" />
          <el-option v-for="u in users" :key="u.id" :label="u.username" :value="u.id" />
        </el-select>
      </div>

      <div v-if="loading && page === 1" class="skeleton-list">
        <div v-for="i in 3" :key="i" class="skeleton-card card">
          <div class="skeleton-header">
            <div class="skeleton skeleton-avatar" />
            <div class="skeleton skeleton-name" />
          </div>
          <div class="skeleton skeleton-line w-3/4" />
          <div class="skeleton skeleton-line w-1/2" />
          <div class="skeleton skeleton-image" />
        </div>
      </div>

      <div v-else-if="!loading && posts.length === 0" class="empty-state">
        <div class="empty-state-icon">📝</div>
        <h3>还没有内容</h3>
        <p>记录宝宝成长的第一个瞬间吧</p>
        <el-button type="primary" @click="goUpload">开始记录</el-button>
      </div>

      <div v-else class="post-list">
        <PostCard v-for="post in posts" :key="post.id" :post="post" @refresh="fetchPosts" />

        <div v-if="hasMore" class="load-more">
          <el-button :loading="loadingMore" @click="loadMore" round plain>
            加载更多
          </el-button>
        </div>
      </div>

      <button class="fab" @click="goUpload" aria-label="发布新内容">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
      </button>
    </main>
  </div>
</template>

<style scoped>
.dashboard-page {
  min-height: 100vh;
  background: var(--color-bg);
}

.dash-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-6);
  flex-wrap: wrap;
  gap: var(--space-3);
}

.page-title {
  margin: 0;
}

.author-filter {
  width: 140px;
}

.skeleton-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.skeleton-card {
  padding: var(--space-5);
}

.skeleton-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.skeleton-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
}

.skeleton-name {
  width: 100px;
  height: 14px;
}

.skeleton-line {
  height: 12px;
  margin-bottom: var(--space-2);
}

.skeleton-image {
  height: 180px;
  margin-top: var(--space-3);
}

.w-3\4 { width: 75%; }
.w-1\2 { width: 50%; }

.post-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.load-more {
  text-align: center;
  padding: var(--space-4) 0 var(--space-8);
}

.fab {
  position: fixed;
  bottom: 28px;
  right: 28px;
  width: 52px;
  height: 52px;
  border-radius: 50%;
  border: none;
  background: var(--color-primary);
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 14px rgba(64, 158, 255, 0.35);
  transition: transform 0.15s, box-shadow 0.15s;
  z-index: 100;
}

.fab:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(64, 158, 255, 0.45);
}

.fab:active {
  transform: scale(0.95);
}

@media (max-width: 768px) {
  .fab {
    bottom: 20px;
    right: 20px;
    width: 48px;
    height: 48px;
  }
}
</style>
