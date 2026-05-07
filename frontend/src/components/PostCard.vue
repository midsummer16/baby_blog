<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { toggleLike } from '@/api'
import { useAuthStore } from '@/stores/auth'
import dayjs from 'dayjs'

const props = defineProps({
  post: { type: Object, required: true },
})

const emit = defineEmits(['refresh'])

const router = useRouter()
const auth = useAuthStore()

const isLiked = computed(() => props.post.is_liked)
const likeCount = computed(() => props.post.like_count ?? 0)
const commentCount = computed(() => props.post.comment_count ?? 0)
const blessingCount = computed(() => props.post.blessing_count ?? 0)

const images = computed(() => props.post.media?.filter((m) => m.media_type === 'image') ?? [])
const videos = computed(() => props.post.media?.filter((m) => m.media_type === 'video') ?? [])

const imageGridClass = computed(() => {
  const len = images.value.length
  if (len === 0) return ''
  if (len === 1) return 'grid-cols-1'
  if (len <= 4) return 'grid-cols-2'
  return 'grid-cols-3'
})

const formattedDate = computed(() => dayjs(props.post.created_at).format('YYYY-MM-DD HH:mm'))

async function handleLike(e) {
  e.stopPropagation()
  try {
    await toggleLike(props.post.id)
    props.post.is_liked = !props.post.is_liked
    props.post.like_count = (props.post.like_count ?? 0) + (props.post.is_liked ? 1 : -1)
    emit('refresh')
  } catch {
    ElMessage.error('操作失败')
  }
}

function goToDetail() {
  router.push(`/post/${props.post.id}`)
}
</script>

<template>
  <article class="post-card card" @click="goToDetail" role="button" tabindex="0" @keydown.enter="goToDetail">
    <div class="post-header">
      <el-avatar :size="36" :src="post.author?.avatar" class="post-avatar" />
      <div class="post-meta">
        <span class="post-author">{{ post.author?.username }}</span>
        <span class="post-date">{{ formattedDate }}</span>
      </div>
    </div>

    <p v-if="post.content" class="post-text">{{ post.content }}</p>

    <div v-if="post.tags?.length" class="post-tags">
      <span v-for="tag in post.tags" :key="tag" class="tag">{{ tag }}</span>
    </div>

    <div v-if="images.length" :class="['image-grid', imageGridClass]">
      <el-image
        v-for="(img, idx) in images"
        :key="idx"
        :src="img.file || img.url"
        :preview-src-list="images.map(i => i.file || i.url)"
        fit="cover"
        lazy
        class="grid-image"
        :class="{ 'grid-image-span': images.length === 1 }"
      />
    </div>

    <div v-if="videos.length" class="post-videos">
      <video
        v-for="(vid, idx) in videos"
        :key="idx"
        :src="vid.file || vid.url"
        controls
        class="post-video"
        preload="metadata"
      />
    </div>

    <div class="post-actions" @click.stop>
      <button class="action-btn" :class="{ liked: isLiked }" @click="handleLike" aria-label="点赞">
        <svg v-if="isLiked" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
        <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
        <span>{{ likeCount }}</span>
      </button>
      <button class="action-btn" @click.stop="goToDetail" aria-label="评论">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        <span>{{ commentCount }}</span>
      </button>
      <button class="action-btn" @click.stop="goToDetail" aria-label="祝福">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
        <span>{{ blessingCount }}</span>
      </button>
    </div>
  </article>
</template>

<style scoped>
.post-card {
  margin-bottom: var(--space-4);
  padding: var(--space-5);
  cursor: pointer;
  border-radius: var(--radius-md);
}

.post-card:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.post-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-3);
}

.post-avatar {
  flex-shrink: 0;
}

.post-meta {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.post-author {
  font-weight: 600;
  font-size: var(--font-sm);
  color: var(--color-text);
}

.post-date {
  font-size: var(--font-xs);
  color: var(--color-text-muted);
}

.post-text {
  font-size: var(--font-base);
  line-height: 1.6;
  margin: 0 0 var(--space-3);
  white-space: pre-wrap;
  color: var(--color-text);
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-1);
  margin-bottom: var(--space-3);
}

.tag {
  display: inline-block;
  padding: 2px var(--space-2);
  font-size: var(--font-xs);
  background: var(--color-primary-light);
  color: var(--color-primary);
  border-radius: 100px;
  font-weight: 500;
}

.image-grid {
  display: grid;
  gap: 3px;
  margin-bottom: var(--space-3);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.grid-cols-1 { grid-template-columns: 1fr; }
.grid-cols-2 { grid-template-columns: 1fr 1fr; }
.grid-cols-3 { grid-template-columns: 1fr 1fr 1fr; }

.grid-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  transition: opacity 0.2s;
}

.grid-image-span {
  max-height: 360px;
  height: auto;
}

.post-videos {
  margin-bottom: var(--space-3);
}

.post-video {
  width: 100%;
  max-height: 400px;
  border-radius: var(--radius-sm);
}

.post-actions {
  display: flex;
  gap: var(--space-2);
  padding-top: var(--space-3);
  border-top: 1px solid var(--color-border-light);
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-1) var(--space-3);
  border: none;
  background: transparent;
  border-radius: var(--radius-sm);
  font-size: var(--font-sm);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all 0.15s;
}

.action-btn:hover {
  background: var(--color-surface-hover);
  color: var(--color-primary);
}

.action-btn.liked {
  color: var(--color-like);
}

.action-btn.liked:hover {
  background: #fef0f0;
}

.action-btn span {
  font-weight: 500;
}
</style>
