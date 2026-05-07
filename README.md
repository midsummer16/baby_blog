# BabyBlog - 宝宝时光轴

基于 Django + Vue 3 的宝宝成长记录博客，Docker 一键部署。

## 技术栈

| 层 | 技术 |
|---|---|
| 后端 | Django 4.2 + Django REST Framework + JWT |
| 前端 | Vue 3 + Vite + Element Plus + Pinia |
| 数据库 | SQLite |
| 部署 | Docker + Docker Compose |

## 功能

- 用户注册/登录（JWT认证）
- 时光轴：图文视频发布、标签、媒体上传
- 成长里程碑：翻身/坐/爬/走路/说话/长牙等
- 社交互动：点赞、评论、祝福
- 历史今日：查看历年今日记录
- 搜索：按内容和标签检索
- 个人信息管理：头像、资料编辑

## 快速开始

```bash
git clone git@github.com:midsummer16/baby_blog.git
cd baby_blog
docker compose up --build
```

访问 http://localhost:11118

默认管理员：`admin` / `admin`

## 文件上传限制

| 类型 | 上限 |
|---|---|
| 图片 (jpg/png) | 20MB |
| 视频 (mp4/webm) | 200MB |

## 项目结构

```
BabyBlog/
├── backend/                # Django 后端
│   ├── apps/
│   │   ├── accounts/       # 用户管理
│   │   ├── posts/          # 文章、媒体、里程碑
│   │   └── social/         # 评论、点赞、祝福
│   └── babyblog/           # Django 配置
├── frontend/               # Vue 3 前端
│   └── src/
│       ├── components/     # 通用组件
│       ├── views/          # 页面
│       ├── stores/         # Pinia 状态
│       ├── api/            # API 封装
│       └── router/         # 路由
├── docker-compose.yml
├── Dockerfile
└── docker-entrypoint.sh
```

## 数据持久化

- 数据库：Docker volume `db_data` → `/app/data`
- 上传文件：Docker volume `media_data` → `/app/media`

重建镜像不会丢失数据，除非执行 `docker compose down -v`。
