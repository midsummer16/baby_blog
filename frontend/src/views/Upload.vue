<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { createPost, uploadMedia, createMilestone } from '@/api'
import NavBar from '@/components/NavBar.vue'

const router = useRouter()

const content = ref('')
const tags = ref([])
const tagInput = ref('')
const files = ref([])
const uploading = ref(false)
const uploadProgress = ref(0)
const showMilestone = ref(false)

const milestoneForm = reactive({
  type: '',
  date: '',
})

const milestoneTypes = [
  { value: 'roll_over', label: '翻身' },
  { value: 'sit', label: '坐' },
  { value: 'crawl', label: '爬' },
  { value: 'walk', label: '走路' },
  { value: 'speak', label: '说话' },
  { value: 'tooth', label: '长牙' },
  { value: 'wean', label: '断奶' },
  { value: 'kindergarten', label: '上幼儿园' },
  { value: 'other', label: '其他' },
]

function addTag() {
  const val = tagInput.value.trim()
  if (!val) return
  if (tags.value.includes(val)) {
    ElMessage.warning('标签已存在')
    return
  }
  tags.value.push(val)
  tagInput.value = ''
}

function removeTag(tag) {
  tags.value = tags.value.filter((t) => t !== tag)
}

function handleFileChange(uploadFile) {
  const file = uploadFile.raw
  const maxSize = 20 * 1024 * 1024
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'video/mp4', 'video/webm']

  if (!allowedTypes.includes(file.type)) {
    ElMessage.error('不支持的文件类型，仅支持 jpg/png/mp4/webm')
    return false
  }

  if (file.size > maxSize) {
    ElMessage.error('文件大小不能超过 20MB')
    return false
  }

  const reader = new FileReader()
  reader.onload = (e) => {
    files.value.push({
      raw: file,
      preview: e.target.result,
      type: file.type.startsWith('video') ? 'video' : 'image',
      uploaded: false,
      mediaId: null,
    })
  }
  reader.readAsDataURL(file)
  return false
}

function removeFile(index) {
  files.value.splice(index, 1)
}

async function handleSubmit() {
  if (!content.value.trim() && files.value.length === 0) {
    ElMessage.warning('请输入内容或选择文件')
    return
  }

  uploading.value = true
  uploadProgress.value = 0

  try {
    const mediaIds = []

    for (let i = 0; i < files.value.length; i++) {
      uploadProgress.value = Math.round((i / files.value.length) * 50)
      const formData = new FormData()
      formData.append('file', files.value[i].raw)
      const res = await uploadMedia(formData)
      mediaIds.push(res.data.id)
    }

    uploadProgress.value = 75

    const postData = {
      content: content.value.trim(),
      tags: tags.value,
      media_ids: mediaIds,
    }

    if (showMilestone.value && milestoneForm.type) {
      postData.milestone_type = milestoneForm.type
      postData.milestone_date = milestoneForm.date
    }

    const postRes = await createPost(postData)
    uploadProgress.value = 100

    if (showMilestone.value && milestoneForm.type) {
      try {
        await createMilestone({
          milestone_type: milestoneForm.type,
          achieved_date: milestoneForm.date || new Date().toISOString().split('T')[0],
          post: postRes.data.id,
        })
      } catch {
        // milestone creation is optional
      }
    }

    ElMessage.success('发布成功')
    router.push('/dashboard')
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '发布失败')
  } finally {
    uploading.value = false
  }
}
</script>

<template>
  <div class="upload-page">
    <NavBar />

    <div class="upload-content">
      <h2 class="page-title">📝 记录新内容</h2>

      <el-card shadow="never" class="upload-card">
        <el-form label-position="top">
          <el-form-item label="内容">
            <el-input
              v-model="content"
              type="textarea"
              :rows="5"
              placeholder="记录宝宝的成长时刻..."
              maxlength="5000"
              show-word-limit
            />
          </el-form-item>

          <el-form-item label="标签">
            <div class="tag-input-area">
              <el-input
                v-model="tagInput"
                placeholder="输入标签后按回车添加"
                @keyup.enter="addTag"
                class="tag-input"
              >
                <template #append>
                  <el-button @click="addTag">添加</el-button>
                </template>
              </el-input>
              <div class="tag-list" v-if="tags.length">
                <el-tag
                  v-for="tag in tags"
                  :key="tag"
                  closable
                  @close="removeTag(tag)"
                  class="tag-item"
                >{{ tag }}</el-tag>
              </div>
            </div>
          </el-form-item>

          <el-form-item label="图片/视频">
            <el-upload
              action=""
              :auto-upload="false"
              :show-file-list="false"
              :on-change="handleFileChange"
              accept="image/jpeg,image/jpg,image/png,video/mp4,video/webm"
              multiple
            >
              <div class="upload-area">
                <el-icon :size="48"><Plus /></el-icon>
                <p>点击或拖拽文件到此处上传</p>
                <p class="upload-hint">支持 jpg/png/mp4/webm，单个文件不超过 20MB</p>
              </div>
            </el-upload>

            <div v-if="files.length" class="file-preview-list">
              <div
                v-for="(file, idx) in files"
                :key="idx"
                class="file-preview-item"
              >
                <img
                  v-if="file.type === 'image'"
                  :src="file.preview"
                  class="preview-thumb"
                />
                <video
                  v-else
                  :src="file.preview"
                  class="preview-thumb"
                  muted
                />
                <el-button
                  circle
                  size="small"
                  type="danger"
                  class="remove-file-btn"
                  @click="removeFile(idx)"
                >
                  <el-icon><Close /></el-icon>
                </el-button>
              </div>
            </div>
          </el-form-item>

          <el-form-item>
            <el-collapse v-model="showMilestone" class="milestone-collapse">
              <el-collapse-item title="🏆 添加里程碑" name="milestone">
                <el-form-item label="里程碑类型">
                  <el-select v-model="milestoneForm.type" placeholder="选择里程碑类型">
                    <el-option
                      v-for="mt in milestoneTypes"
                      :key="mt.value"
                      :label="mt.label"
                      :value="mt.value"
                    />
                  </el-select>
                </el-form-item>
                <el-form-item label="里程碑日期">
                  <el-date-picker
                    v-model="milestoneForm.date"
                    type="date"
                    placeholder="选择日期"
                    format="YYYY-MM-DD"
                    value-format="YYYY-MM-DD"
                  />
                </el-form-item>
              </el-collapse-item>
            </el-collapse>
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="uploading"
              @click="handleSubmit"
              class="submit-btn"
            >发布</el-button>
            <el-button size="large" @click="router.push('/dashboard')">取消</el-button>
          </el-form-item>

          <el-progress
            v-if="uploading"
            :percentage="uploadProgress"
            :stroke-width="8"
            class="upload-progress"
          />
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.upload-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding-top: 60px;
}
.upload-content {
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
.upload-card {
  border-radius: 12px;
  padding: 16px;
}
.tag-input-area {
  width: 100%;
}
.tag-list {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.tag-item {
  margin-right: 0;
}
.upload-area {
  border: 2px dashed #d9d9d9;
  border-radius: 12px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  color: #999;
}
.upload-area:hover {
  border-color: #409eff;
  color: #409eff;
  background: #f0f5ff;
}
.upload-area p {
  margin: 8px 0 0;
  font-size: 14px;
}
.upload-hint {
  font-size: 12px !important;
  color: #bbb !important;
}
.file-preview-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 12px;
}
.file-preview-item {
  position: relative;
  width: 120px;
  height: 120px;
}
.preview-thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}
.remove-file-btn {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 24px;
  height: 24px;
}
.milestone-collapse {
  width: 100%;
}
.submit-btn {
  margin-right: 12px;
}
.upload-progress {
  margin-top: 16px;
}
</style>
