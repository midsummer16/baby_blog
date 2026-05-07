# BabyBlog Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan.

**Goal:** Build a Docker-deployable baby blog with Django DRF backend and Vue 3 frontend.

**Architecture:** Single Docker container running Django + SQLite + compiled Vue SPA. Django serves the API via DRF and the Vue SPA via WhiteNoise. SQLite and media files are persisted via Docker volumes.

**Tech Stack:** Django 4.2, Django REST Framework, SQLite, Vue 3, Vite, Element Plus, Docker

---

### Task 1: Project Scaffolding

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/manage.py`
- Create: `backend/babyblog/settings.py`
- Create: `backend/babyblog/urls.py`
- Create: `backend/babyblog/wsgi.py`
- Create: `backend/babyblog/__init__.py`
- Create: `Dockerfile`
- Create: `docker-compose.yml`
- Create: `.dockerignore`

### Task 2: Accounts App (User Management)

**Files:**
- Create: `backend/apps/accounts/models.py`
- Create: `backend/apps/accounts/serializers.py`
- Create: `backend/apps/accounts/views.py`
- Create: `backend/apps/accounts/urls.py`
- Create: `backend/apps/accounts/admin.py`
- Create: `backend/apps/accounts/__init__.py`
- Create: `backend/apps/accounts/management/commands/initadmin.py`

### Task 3: Posts & Media Apps

**Files:**
- Create: `backend/apps/posts/models.py`
- Create: `backend/apps/posts/serializers.py`
- Create: `backend/apps/posts/views.py`
- Create: `backend/apps/posts/urls.py`
- Create: `backend/apps/posts/admin.py`
- Create: `backend/apps/posts/__init__.py`

### Task 4: Milestones & Social Apps

**Files:**
- Create: `backend/apps/social/models.py`
- Create: `backend/apps/social/serializers.py`
- Create: `backend/apps/social/views.py`
- Create: `backend/apps/social/urls.py`
- Create: `backend/apps/social/admin.py`
- Create: `backend/apps/social/__init__.py`

### Task 5: Vue Frontend Scaffolding

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.js`
- Create: `frontend/index.html`
- Create: `frontend/src/main.js`
- Create: `frontend/src/App.vue`
- Create: `frontend/src/router/index.js`
- Create: `frontend/src/stores/`
- Create: `frontend/src/api/`
- Create: `frontend/src/views/`

### Task 6: Vue Views

**Files:**
- Create: `frontend/src/views/Login.vue`
- Create: `frontend/src/views/Dashboard.vue`
- Create: `frontend/src/views/Upload.vue`
- Create: `frontend/src/views/Milestones.vue`
- Create: `frontend/src/views/PostDetail.vue`
- Create: `frontend/src/views/Search.vue`
- Create: `frontend/src/views/Profile.vue`
- Create: `frontend/src/views/OnThisDay.vue`
