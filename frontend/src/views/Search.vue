<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { searchPosts, getUsers } from '@/api'
import PostCard from '@/components/PostCard.vue'
import NavBar from '@/components/NavBar.vue'

const router = useRouter()

const query = ref('')
const dateFrom = ref('')
const dateTo = ref('')
const tags = ref([])
const tagInput = ref('')
const author = ref('')
const users = ref([])
const results = ref([])
const loading = ref(false)
const searched = ref(false)
const showAdvanced = ref(false)

async function fetchUsers() {
  try {
    const res = await getUsers()
    users.value = res.data.results ?? res.data
  } catch {
    // ignore
  }
}

function addTag() {
  const val = tagInput.value.trim()
  if (!val) return
  if (!tags.value.includes(val)) {
    tags.value.push(val)
  }
  tagInput.value = ''
}

function removeTag(tag) {
  tags.value = tags.value.filter((t) => t !== tag)
}

async function handleSearch() {
  loading.value = true
  searched.value = true
  try {
    const params = {}
    if (query.value.trim()) params.q = query.value.trim()
    if (dateFrom.value) params.date_from = dateFrom.value
    if (dateTo.value) params.date_to = dateTo.value
    if (tags.value.length) params.tags = JSON.stringify(tags.value)
    if (author.value) params.author = author.value

    const res = await searchPosts(params)
    results.value = res.data.results ?? res.data
  } catch {
    ElMessage.error('搜索失败')
  } finally {
    loading.value = false
  }
}

function refreshResults() {
  // no-op for post card refresh
}

onMounted(() => {
  fetchUsers()
})
</script>

<template>
  <div class="search-page">
    <NavBar />

    <div class="search-content">
      <h2 class="page-title">🔍 搜索</h2>

      <el-card shadow="never" class="search-card">
        <div class="search-main">
          <el-input
            v-model="query"
            placeholder="搜索内容..."
            size="large"
            clearable
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
            <template #append>
              <el-button @click="handleSearch" :loading="loading">搜索</el-button>
            </template>
          </el-input>
        </div>

        <div class="advanced-toggle">
          <el-button text @click="showAdvanced = !showAdvanced">
            {{ showAdvanced ? '收起高级筛选' : '高级筛选' }}
            <el-icon><ArrowDown v-if="!showAdvanced" /><ArrowUp v-else /></el-icon>
          </el-button>
        </div>

        <transition name="fade">
          <div v-if="showAdvanced" class="advanced-filters">
            <el-form label-position="top" class="filter-form">
              <el-row :gutter="16">
                <el-col :span="12">
                  <el-form-item label="开始日期">
                    <el-date-picker
                      v-model="dateFrom"
                      type="date"
                      placeholder="开始日期"
                      format="YYYY-MM-DD"
                      value-format="YYYY-MM-DD"
                      style="width:100%"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="结束日期">
                    <el-date-picker
                      v-model="dateTo"
                      type="date"
                      placeholder="结束日期"
                      format="YYYY-MM-DD"
                      value-format="YYYY-MM-DD"
                      style="width:100%"
                    />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-form-item label="标签">
                <div class="tag-filter-area">
                  <el-input
                    v-model="tagInput"
                    placeholder="输入标签后按回车"
                    @keyup.enter="addTag"
                    size="small"
                  >
                    <template #append>
                      <el-button @click="addTag" size="small">添加</el-button>
                    </template>
                  </el-input>
                  <div v-if="tags.length" class="tag-list">
                    <el-tag
                      v-for="tag in tags"
                      :key="tag"
                      closable
                      @close="removeTag(tag)"
                      size="small"
                    >{{ tag }}</el-tag>
                  </div>
                </div>
              </el-form-item>

              <el-form-item label="作者">
                <el-select v-model="author" placeholder="全部作者" clearable style="width:100%">
                  <el-option label="全部作者" value="" />
                  <el-option
                    v-for="u in users"
                    :key="u.id"
                    :label="u.username"
                    :value="u.id"
                  />
                </el-select>
              </el-form-item>
            </el-form>
          </div>
        </transition>
      </el-card>

      <div v-loading="loading" class="search-results">
        <div v-if="searched && !loading && results.length === 0" class="empty-state">
          <el-empty description="没有找到相关内容" />
        </div>

        <PostCard
          v-for="post in results"
          :key="post.id"
          :post="post"
          @refresh="refreshResults"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.search-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding-top: 60px;
}
.search-content {
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
.search-card {
  border-radius: 12px;
  padding: 8px 16px;
  margin-bottom: 24px;
}
.search-main {
  margin-bottom: 8px;
}
.advanced-toggle {
  text-align: center;
  margin-bottom: 8px;
}
.filter-form {
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}
.tag-filter-area {
  width: 100%;
}
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 8px;
}
.search-results {
  min-height: 200px;
}
.empty-state {
  padding: 60px 0;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
