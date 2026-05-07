import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin, register as apiRegister, getMe, updateMe, uploadAvatar as apiUploadAvatar } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(null)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  async function login(credentials) {
    const response = await apiLogin(credentials)
    token.value = response.data.tokens?.access
    localStorage.setItem('token', token.value)
    await fetchMe()
    return response
  }

  async function register(data) {
    const response = await apiRegister(data)
    if (response.data.tokens?.access) {
      token.value = response.data.tokens.access
      localStorage.setItem('token', token.value)
      await fetchMe()
    }
    return response
  }

  async function fetchMe() {
    try {
      const response = await getMe()
      user.value = response.data
    } catch {
      logout()
    }
  }

  async function updateProfile(data) {
    const response = await updateMe(data)
    user.value = response.data
    return response
  }

  async function uploadAvatar(file) {
    const formData = new FormData()
    formData.append('avatar', file)
    const response = await apiUploadAvatar(formData)
    user.value = response.data
    return response
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
  }

  return {
    token,
    user,
    isAuthenticated,
    isAdmin,
    login,
    register,
    fetchMe,
    updateProfile,
    uploadAvatar,
    logout,
  }
})
