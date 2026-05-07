<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getPost, deletePost, toggleLike,
  getComments, createComment,
  getBlessings, createBlessing,
} from '@/api'
import { useAuthStore } from '@/stores/auth'
import NavBar from '@/components/NavBar.vue'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const post = ref(null)
const comments = ref([])
const blessings = ref([])
const loading = ref(true)
const commentText = ref('')
const blessingText = ref('')
const submittingComment = ref(false)
const submittingBlessing = ref(false)

const isAuthor = computed(() => {
  if (!post.value || !auth.user) return false
  const postAuthorId = post.value.author?.id ?? post.value.author
  return postAuthorId === auth.user.id
})

const images = computed(() => {
  return post.value?.media?.filter((m) => m.media_type === 'image') ?? []
})

const videos = computed(() => {
  return post.value?.media?.filter((m) => m.media_type === 'video') ?? []
})

async function fetchPost() {
  try {
    const res = await getPost(route.params.id)
    post.value = res.data
  } catch {
    ElMessage.error('加载失败')
    router.push('/dashboard')
  } finally {
    loading.value = false
  }
}

async function fetchComments() {
  try {
    const res = await getComments(route.params.id)
    comments.value = res.data.results ?? res.data
  } catch {
    // ignore
  }
}

async function fetchBlessings() {
  try {
    const res = await getBlessings(route.params.id)
    blessings.value = res.data.results ?? res.data
  } catch {
    // ignore
  }
}

async function handleLike() {
  try {
    await toggleLike(post.value.id)
    post.value.is_liked = !post.value.is_liked
    post.value.like_count = (post.value.like_count ?? 0) + (post.value.is_liked ? 1 : -1)
  } catch {
    ElMessage.error('操作失败')
  }
}

async function handleDelete() {
  try {
    await ElMessageBox.confirm('确定删除这篇文章吗？', '确认删除', {
      type: 'warning',
      confirmButtonText: '删除',
      cancelButtonText: '取消',
    })
    await deletePost(post.value.id)
    ElMessage.success('删除成功')
    router.push('/dashboard')
  } catch {
    // cancelled
  }
}

async function handleComment() {
  if (!commentText.value.trim()) return
  submittingComment.value = true
  try {
    await createComment(route.params.id, { content: commentText.value.trim() })
    ElMessage.success('评论成功')
    commentText.value = ''
    fetchComments()
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '评论失败')
  } finally {
    submittingComment.value = false
  }
}

async function handleBlessing() {
  if (!blessingText.value.trim()) return
  submittingBlessing.value = true
  try {
    await createBlessing(route.params.id, { content: blessingText.value.trim() })
    ElMessage.success('祝福已发送')
    blessingText.value = ''
    fetchBlessings()
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '发送失败')
  } finally {
    submittingBlessing.value = false
  }
}

function goBack() {
  router.back()
}

function formattedDate(date) {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

onMounted(() => {
  fetchPost()
  fetchComments()
  fetchBlessings()
})
</script>

<template>
  <div class="post-detail-page">
    <NavBar />

    <div class="detail-content" v-loading="loading">
      <div class="back-bar">
        <el-button text @click="goBack">
          <el-icon><ArrowLeft /></el-icon>返回
        </el-button>
      </div>

      <div v-if="post" class="post-detail-main">
        <el-card shadow="never" class="detail-card">
          <div class="post-header">
            <el-avatar :size="48" :src="post.author?.avatar" />
            <div class="post-author-info">
              <span class="post-author-name">{{ post.author?.username }}</span>
              <span class="post-date">{{ formattedDate(post.created_at) }}</span>
            </div>
            <div class="post-actions-top" v-if="isAuthor">
              <el-button type="danger" text @click="handleDelete">
                <el-icon><Delete /></el-icon>删除
              </el-button>
            </div>
          </div>

          <div class="post-content" v-if="post.content">{{ post.content }}</div>

          <div class="post-tags" v-if="post.tags?.length">
            <el-tag v-for="tag in post.tags" :key="tag" size="small" class="post-tag">{{ tag }}</el-tag>
          </div>

          <div class="post-media-grid" v-if="images.length">
            <el-image
              v-for="(img, idx) in images"
              :key="idx"
              :src="img.file || img.url"
              :preview-src-list="images.map(i => i.file || i.url)"
              fit="contain"
              class="detail-image"
            />
          </div>

          <div class="post-videos" v-if="videos.length">
            <video
              v-for="(vid, idx) in videos"
              :key="idx"
              :src="vid.file || vid.url"
              controls
              class="detail-video"
            />
          </div>

          <div class="post-actions">
            <el-button
              :type="post.is_liked ? 'danger' : 'default'"
              size="large"
              @click="handleLike"
            >
              <el-icon v-if="post.is_liked"><HeartFilled /></el-icon>
              <el-icon v-else><Heart /></el-icon>
              {{ post.like_count ?? 0 }}
            </el-button>
            <el-button size="large">
              <el-icon><ChatDotSquare /></el-icon>
              {{ comments.length }}
            </el-button>
            <el-button size="large">
              <el-icon><Star /></el-icon>
              {{ blessings.length }}
            </el-button>
          </div>
        </el-card>

        <el-divider />

        <el-card shadow="never" class="comments-section" id="comments">
          <template #header>
            <span>评论 ({{ comments.length }})</span>
          </template>

          <div class="add-comment">
            <el-input
              v-model="commentText"
              type="textarea"
              :rows="2"
              placeholder="写下你的评论..."
            />
            <el-button
              type="primary"
              :loading="submittingComment"
              @click="handleComment"
              class="comment-submit"
            >发表评论</el-button>
          </div>

          <div v-if="comments.length === 0" class="empty-section">
            <el-empty description="暂无评论" :image-size="80" />
          </div>

          <div v-for="comment in comments" :key="comment.id" class="comment-item">
            <el-avatar :size="32" :src="comment.author?.avatar" />
            <div class="comment-body">
              <div class="comment-meta">
                <span class="comment-author">{{ comment.author?.username }}</span>
                <span class="comment-date">{{ formattedDate(comment.created_at) }}</span>
              </div>
              <div class="comment-content">{{ comment.content }}</div>
            </div>
          </div>
        </el-card>

        <el-divider />

        <el-card shadow="never" class="blessings-section" id="blessings">
          <template #header>
            <span>🙏 祝福 ({{ blessings.length }})</span>
          </template>

          <div class="add-blessing">
            <el-input
              v-model="blessingText"
              type="textarea"
              :rows="2"
              placeholder="送上你的祝福..."
            />
            <el-button
              type="warning"
              :loading="submittingBlessing"
              @click="handleBlessing"
              class="comment-submit"
            >发送祝福</el-button>
          </div>

          <div v-if="blessings.length === 0" class="empty-section">
            <el-empty description="暂无祝福" :image-size="80" />
          </div>

          <div v-for="blessing in blessings" :key="blessing.id" class="comment-item blessing-item">
            <el-avatar :size="32" :src="blessing.author?.avatar" />
            <div class="comment-body">
              <div class="comment-meta">
                <span class="comment-author">{{ blessing.author?.username }}</span>
                <span class="comment-date">{{ formattedDate(blessing.created_at) }}</span>
              </div>
              <div class="comment-content blessing-content">{{ blessing.content }}</div>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<style scoped>
.post-detail-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding-top: 60px;
}
.detail-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px 16px;
}
.back-bar {
  margin-bottom: 16px;
}
.detail-card {
  padding: 8px;
}
.post-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}
.post-author-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}
.post-author-name {
  font-weight: 600;
  font-size: 15px;
}
.post-date {
  font-size: 12px;
  color: #999;
}
.post-actions-top {
  display: flex;
  gap: 4px;
}
.post-content {
  font-size: 16px;
  line-height: 1.8;
  margin-bottom: 16px;
  white-space: pre-wrap;
}
.post-tags {
  margin-bottom: 16px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.post-tag {
  margin-right: 0;
}
.post-media-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 8px;
  margin-bottom: 16px;
}
.detail-image {
  width: 100%;
  border-radius: 8px;
}
.post-videos {
  margin-bottom: 16px;
}
.detail-video {
  width: 100%;
  max-height: 500px;
  border-radius: 8px;
}
.post-actions {
  display: flex;
  gap: 12px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}
.comments-section,
.blessings-section {
  padding: 8px;
}
.add-comment,
.add-blessing {
  margin-bottom: 16px;
}
.comment-submit {
  margin-top: 8px;
}
.comment-item {
  display: flex;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f5f5f5;
}
.comment-item:last-child {
  border-bottom: none;
}
.comment-body {
  flex: 1;
}
.comment-meta {
  display: flex;
  gap: 8px;
  margin-bottom: 4px;
}
.comment-author {
  font-weight: 600;
  font-size: 13px;
}
.comment-date {
  font-size: 12px;
  color: #999;
}
.comment-content {
  font-size: 14px;
  line-height: 1.5;
}
.blessing-content {
  color: #e6a23c;
}
.empty-section {
  padding: 20px 0;
}
</style>
