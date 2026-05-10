<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const mobileOpen = ref(false)

const activeRouteName = computed(() => route.name)

const navItems = [
  { name: 'Dashboard', label: '时光轴', icon: 'Clock' },
  { name: 'Upload', label: '上传', icon: 'Upload' },
  { name: 'Milestones', label: '里程碑', icon: 'TrophyBase' },
  { name: 'Search', label: '搜索', icon: 'Search' },
  { name: 'OnThisDay', label: '历史今日', icon: 'Histogram' },
]

function go(name) {
  router.push({ name })
  mobileOpen.value = false
}

function goProfile() {
  router.push('/profile')
}

function logout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <header class="navbar">
    <div class="navbar-inner">
      <div class="brand" @click="go('Dashboard')" role="button" tabindex="0" @keydown.enter="go('Dashboard')">
        <span class="brand-icon">👶</span>
        <span class="brand-text">宝宝时光轴</span>
      </div>

      <nav class="nav-links" role="navigation" aria-label="主导航">
        <button
          v-for="item in navItems"
          :key="item.name"
          :class="['nav-link', { active: activeRouteName === item.name }]"
          @click="go(item.name)"
        >
          <el-icon><component :is="item.icon" /></el-icon>
          <span>{{ item.label }}</span>
        </button>
      </nav>

      <div class="nav-right">
        <el-dropdown trigger="click" placement="bottom-end">
          <button class="user-btn" aria-label="用户菜单">
            <el-avatar :size="30" :src="auth.user?.avatar" />
            <span class="user-name">{{ auth.user?.username }}</span>
          </button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item v-if="auth.isAdmin" @click="go('UserManage')">
                <el-icon><Setting /></el-icon>用户管理
              </el-dropdown-item>
              <el-dropdown-item @click="goProfile">
                <el-icon><User /></el-icon>个人信息
              </el-dropdown-item>
              <el-dropdown-item divided @click="logout">
                <el-icon><SwitchButton /></el-icon>退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>

        <button class="mobile-toggle" @click="mobileOpen = !mobileOpen" aria-label="菜单">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </button>
      </div>
    </div>

    <transition name="slide">
      <div v-if="mobileOpen" class="mobile-menu">
        <button
          v-for="item in navItems"
          :key="item.name"
          :class="['mobile-link', { active: activeRouteName === item.name }]"
          @click="go(item.name)"
        >
          <el-icon><component :is="item.icon" /></el-icon>
          {{ item.label }}
        </button>
        <button v-if="auth.isAdmin" class="mobile-link" @click="go('UserManage')">
          <el-icon><Setting /></el-icon>
          用户管理
        </button>
      </div>
    </transition>
  </header>
</template>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: var(--color-surface, #fff);
  border-bottom: 1px solid var(--color-border, #e8eaed);
}

.navbar-inner {
  display: flex;
  align-items: center;
  height: 56px;
  padding: 0 var(--space-5);
  max-width: 1200px;
  margin: 0 auto;
  gap: var(--space-4);
}

.brand {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  cursor: pointer;
  flex-shrink: 0;
}

.brand-icon {
  font-size: 1.5rem;
  line-height: 1;
}

.brand-text {
  font-size: var(--font-lg);
  font-weight: 700;
  color: var(--color-primary, #409eff);
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 2px;
  flex: 1;
}

.nav-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-2) var(--space-3);
  border: none;
  background: transparent;
  border-radius: var(--radius-sm, 6px);
  font-size: var(--font-sm, 0.875rem);
  color: var(--color-text-secondary, #6b7280);
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}

.nav-link:hover {
  background: var(--color-surface-hover, #f8f9fb);
  color: var(--color-text, #1d1d1f);
}

.nav-link.active {
  background: var(--color-primary-light, #ecf5ff);
  color: var(--color-primary, #409eff);
  font-weight: 600;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  flex-shrink: 0;
}

.user-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-1) var(--space-2);
  border: none;
  background: transparent;
  border-radius: var(--radius-sm, 6px);
  cursor: pointer;
  transition: background 0.15s;
}

.user-btn:hover {
  background: var(--color-surface-hover, #f8f9fb);
}

.user-name {
  font-size: var(--font-sm, 0.875rem);
  color: var(--color-text, #1d1d1f);
  font-weight: 500;
}

.mobile-toggle {
  display: none;
  padding: var(--space-1);
  border: none;
  background: transparent;
  cursor: pointer;
  color: var(--color-text-secondary, #6b7280);
  border-radius: var(--radius-sm, 6px);
}

.mobile-toggle:hover {
  background: var(--color-surface-hover, #f8f9fb);
}

.mobile-menu {
  background: var(--color-surface, #fff);
  border-bottom: 1px solid var(--color-border, #e8eaed);
  padding: var(--space-2);
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.mobile-link {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border: none;
  background: transparent;
  border-radius: var(--radius-sm, 6px);
  font-size: var(--font-base, 1rem);
  color: var(--color-text-secondary, #6b7280);
  cursor: pointer;
  width: 100%;
  text-align: left;
}

.mobile-link.active {
  background: var(--color-primary-light, #ecf5ff);
  color: var(--color-primary, #409eff);
  font-weight: 600;
}

.slide-enter-active, .slide-leave-active {
  transition: max-height 0.25s ease, opacity 0.2s;
  overflow: hidden;
}
.slide-enter-from, .slide-leave-to {
  max-height: 0;
  opacity: 0;
}
.slide-enter-to, .slide-leave-from {
  max-height: 300px;
  opacity: 1;
}

@media (max-width: 768px) {
  .nav-links { display: none; }
  .user-name { display: none; }
  .mobile-toggle { display: flex; }
}

@media (min-width: 769px) {
  .mobile-menu { display: none; }
}
</style>
