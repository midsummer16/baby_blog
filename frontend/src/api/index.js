import axios from 'axios'
import router from '@/router'

const api = axios.create({
  baseURL: '',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token')
      router.push('/login')
    }
    return Promise.reject(error)
  }
)

export function login(data) {
  return api.post('/api/login/', data)
}

export function register(data) {
  return api.post('/api/register/', data)
}

export function getMe() {
  return api.get('/api/me/')
}

export function updateMe(data) {
  return api.put('/api/me/', data)
}

export function uploadAvatar(formData) {
  return api.post('/api/me/avatar/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export function getPosts(params) {
  return api.get('/api/posts/', { params })
}

export function getPost(id) {
  return api.get(`/api/posts/${id}/`)
}

export function createPost(data) {
  return api.post('/api/posts/', data)
}

export function updatePost(id, data) {
  return api.put(`/api/posts/${id}/`, data)
}

export function deletePost(id) {
  return api.delete(`/api/posts/${id}/`)
}

export function uploadMedia(formData) {
  return api.post('/api/upload/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export function getMilestones(params) {
  return api.get('/api/milestones/', { params })
}

export function createMilestone(data) {
  return api.post('/api/milestones/', data)
}

export function getMilestoneTimeline() {
  return api.get('/api/milestones/timeline/')
}

export function toggleLike(id) {
  return api.post(`/api/posts/${id}/like/`)
}

export function getComments(id) {
  return api.get(`/api/posts/${id}/comments/`)
}

export function createComment(id, data) {
  return api.post(`/api/posts/${id}/comments/`, data)
}

export function getBlessings(id) {
  return api.get(`/api/posts/${id}/blessings/`)
}

export function createBlessing(id, data) {
  return api.post(`/api/posts/${id}/blessings/`, data)
}

export function searchPosts(params) {
  return api.get('/api/search/', { params })
}

export function getOnThisDay() {
  return api.get('/api/on-this-day/')
}

export function getUsers() {
  return api.get('/api/users/')
}

export function changePassword(data) {
  return api.post('/api/change-password/', data)
}

export default api
